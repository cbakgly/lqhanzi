# -*- coding:utf8 -*-
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status

from ..pagination import NumberPagination
from ..models import KoreanDedup, InterDictDedup, HanziSet
from ..utils import get_pic_url_by_source_pic_name
from ..filters import fields_or_filter_method
from ..enums import getenum_source, getenum_task_business_status, getenum_business_stage
from task_func import assign_task


class KoreanDedupSerializer(serializers.ModelSerializer):

    class Meta:
        model = KoreanDedup
        fields = "__all__"

    def to_representation(self, instance):
        ret = super(KoreanDedupSerializer, self).to_representation(instance)
        ret['hanzi_pic_path'] = get_pic_url_by_source_pic_name(getenum_source('korean'), ret['hanzi_pic_id'])
        ret['variant_type_display'] = instance.get_variant_type_display()
        ret['hanzi_type'] = instance.get_hanzi_type_display()
        return ret


class KoreanDedupFilter(django_filters.FilterSet):

    """
    异体字拆字过滤器
    """
    u_t_span = django_filters.DateTimeFromToRangeFilter(name="u_t")

    class Meta:
        model = KoreanDedup
        fields = "__all__"


class KoreanDedupViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = KoreanDedup.objects.all()
    filter_class = KoreanDedupFilter
    pagination_class = NumberPagination
    serializer_class = KoreanDedupSerializer


class InterDictDedupSerializer(serializers.ModelSerializer):

    class Meta:
        model = InterDictDedup
        fields = "__all__"

    def to_representation(self, instance):
        ret = super(InterDictDedupSerializer, self).to_representation(instance)
        ret['hanzi_pic_path'] = get_pic_url_by_source_pic_name(getenum_source('korean'), ret['hanzi_pic_id'])
        ret['source_display'] = instance.get_source_display()
        ret['is_draft_equals_review_display'] = instance.get_is_draft_equals_review_display()
        ret['is_review_equals_final_display'] = instance.get_is_review_equals_final_display()
        ret['is_checked_display'] = instance.get_is_checked_display()
        ret['is_submitted_display'] = instance.get_is_submitted_display()

        tw_hanzi = ret['inter_dict_dup_hanzi_draft']
        if tw_hanzi and len(tw_hanzi) <= 2:
            ret['is_draft_pic'] = 0
            row = HanziSet.objects.filter(hanzi_char=tw_hanzi, source=getenum_source('taiwan'))
            ret['inter_dict_dup_hanzi_draft_seq_id'] = row[0].seq_id if row else ''
        else:
            ret['is_draft_pic'] = 1
            ret['inter_dict_dup_hanzi_draft_path'] = get_pic_url_by_source_pic_name(getenum_source('taiwan'), tw_hanzi)

        tw_hanzi = ret['inter_dict_dup_hanzi_review']
        if tw_hanzi and len(tw_hanzi) <= 2:
            ret['is_review_pic'] = 0
            row = HanziSet.objects.filter(hanzi_char=tw_hanzi, source=getenum_source('taiwan'))
            ret['inter_dict_dup_hanzi_review_seq_id'] = row[0].seq_id if row else ''
        else:
            ret['is_review_pic'] = 1
            ret['inter_dict_dup_hanzi_review_path'] = get_pic_url_by_source_pic_name(getenum_source('taiwan'), tw_hanzi)

        tw_hanzi = ret['inter_dict_dup_hanzi_final']
        if tw_hanzi and len(tw_hanzi) <= 2:
            ret['is_final_pic'] = 0
            row = HanziSet.objects.filter(hanzi_char=tw_hanzi, source=getenum_source('taiwan'))
            ret['inter_dict_dup_hanzi_final_seq_id'] = row[0].seq_id if row else ''
        else:
            ret['is_final_pic'] = 1
            ret['inter_dict_dup_hanzi_final_path'] = get_pic_url_by_source_pic_name(getenum_source('taiwan'), tw_hanzi)

        return ret


class InterDictDedupFilter(django_filters.FilterSet):

    """
    异体字拆字过滤器
    """
    inter_dict_dup_hanzi = django_filters.CharFilter(name=["inter_dict_dup_hanzi_draft", "inter_dict_dup_hanzi_review", "inter_dict_dup_hanzi_final"], method=fields_or_filter_method)
    u_t_span = django_filters.DateTimeFromToRangeFilter(name="u_t")

    class Meta:
        model = InterDictDedup
        fields = "__all__"


def update_tasks_status(variants_dedup):
    tasks = list(variants_dedup.task.all())
    task_dict = {}
    for t in tasks:
        task_dict[t.business_stage] = t
    draft = task_dict[getenum_business_stage('init')]
    review = task_dict[getenum_business_stage('review')]
    final = task_dict[getenum_business_stage('final')]
    origin_task = draft
    if draft.task_status == getenum_task_business_status("ongoing"):
        draft.task_status = getenum_task_business_status("completed")
        draft.completed_at = timezone.now()
        review.task_status = getenum_task_business_status("to_be_arranged")
        variants_dedup.save()
        draft.save()
        review.save()
    elif review.task_status == getenum_task_business_status("ongoing"):
        review.task_status = getenum_task_business_status("completed")
        review.completed_at = timezone.now()
        final.task_status = getenum_task_business_status("to_be_arranged")
        variants_dedup.is_draft_equals_review = variants_dedup.inter_dict_dup_hanzi_draft is variants_dedup.inter_dict_dup_hanzi_review
        variants_dedup.save()
        review.save()
        final.save()
        origin_task = review
    elif final.task_status == getenum_task_business_status("ongoing"):
        final.task_status = getenum_task_business_status("completed")
        final.completed_at = timezone.now()
        variants_dedup.is_review_equals_final = variants_dedup.inter_dict_dup_hanzi_review is variants_dedup.inter_dict_dup_hanzi_final
        variants_dedup.save()
        final.save()
        origin_task = final
    else:
        pass
    return origin_task

class InterDictDedupViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)

    queryset = InterDictDedup.objects.exclude(inter_dict_dup_hanzi_final='', inter_dict_dup_hanzi_review='', inter_dict_dup_hanzi_draft='')
    filter_class = InterDictDedupFilter
    pagination_class = NumberPagination
    serializer_class = InterDictDedupSerializer

    # 提交
    @detail_route(methods=["PUT", "GET", "PATCH"])
    def submit(self, request, *args, **kwargs):
        variants_dedup = self.get_object()
        serializer = InterDictDedupSerializer(data=request.data)

        if serializer.is_valid():
            origin_task = update_tasks_status(variants_dedup)
            task_ele = origin_task.content_object
            for key in serializer.initial_data.keys():
                setattr(task_ele, key, serializer.initial_data.get(key, getattr(task_ele, key)))
            task_ele.save()
            serializer = self.serializer_class(task_ele)
            return Response(serializer.data)
        else:
            return Response("数据错误！")

            # 提交并转下一条

    @detail_route(methods=["PUT", "GET", "PATCH"])
    def submit_and_next(self, request, *args, **kwargs):
        variants_dedup = self.get_object()
        serializer = InterDictDedupSerializer(data=request.data)

        if serializer.is_valid():
            origin_task = update_tasks_status(variants_dedup)
            task_ele = origin_task.content_object
            for key in serializer.initial_data.keys():
                setattr(task_ele, key, serializer.initial_data.get(key, getattr(task_ele, key)))
            task_ele.save()

            task_package = origin_task.task_package
            task_plan = task_package.size
            task_num = len(list(task_package.tasks.all()))
            if task_num < task_plan:
                business_type = origin_task.business_type
                business_stage = origin_task.business_stage
                user = origin_task.user
                new_task = assign_task(business_type, business_stage, task_package, user)
                if new_task:
                    serializer = self.serializer_class(new_task.content_object)
                    return Response(serializer.data)
                else:
                    return Response(u"没有更多任务了！", status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(u"该任务包已完成，请领取新任务包。", status=status.HTTP_100_CONTINUE)
        return Response("数据错误！")