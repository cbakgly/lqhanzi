# -*- coding:utf8 -*-
import django_filters
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from ..pagination import NumberPagination
from ..models import InterDictDedup, HanziSet
from ..utils import get_pic_url_by_source_pic_name
from ..filters import fields_or_filter_method
from ..enums import getenum_source, getenum_task_status, getenum_business_stage
from task_func import create_task
from ..functional import timeout_cache
from ..auth import IsBusinessMember


class InterDictDedupSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterDictDedup
        fields = "__all__"

    @timeout_cache(5*60)
    def get_tw_char_seq_id(self, char):
        if char is None or char == '':
            return ''

        row = HanziSet.objects.filter(hanzi_char=char, source=getenum_source('taiwan'))
        return row[0].seq_id if row else ''

    def to_representation(self, instance):
        ret = super(InterDictDedupSerializer, self).to_representation(instance)
        ret['hanzi_pic_path'] = get_pic_url_by_source_pic_name(getenum_source('korean'), ret['hanzi_pic_id'])
        ret['std_hanzi_pic_path'] = get_pic_url_by_source_pic_name(getenum_source('korean'), ret['std_hanzi'])
        ret['source_display'] = instance.get_source_display()
        ret['is_draft_equals_review_display'] = instance.get_is_draft_equals_review_display()
        ret['is_review_equals_final_display'] = instance.get_is_review_equals_final_display()
        ret['is_checked_display'] = instance.get_is_checked_display()
        ret['is_submitted_display'] = instance.get_is_submitted_display()

        tw_hanzi = ret['inter_dict_dup_hanzi_draft']
        if tw_hanzi and len(tw_hanzi) <= 2:
            ret['is_draft_pic'] = 0
            ret['inter_dict_dup_hanzi_draft_seq_id'] = self.get_tw_char_seq_id(tw_hanzi)
        else:
            ret['is_draft_pic'] = 1
            ret['inter_dict_dup_hanzi_draft_path'] = get_pic_url_by_source_pic_name(getenum_source('taiwan'), tw_hanzi)

        tw_hanzi = ret['inter_dict_dup_hanzi_review']
        if tw_hanzi and len(tw_hanzi) <= 2:
            ret['is_review_pic'] = 0
            ret['inter_dict_dup_hanzi_review_seq_id'] = self.get_tw_char_seq_id(tw_hanzi)
        else:
            ret['is_review_pic'] = 1
            ret['inter_dict_dup_hanzi_review_path'] = get_pic_url_by_source_pic_name(getenum_source('taiwan'), tw_hanzi)

        tw_hanzi = ret['inter_dict_dup_hanzi_final']
        if tw_hanzi and len(tw_hanzi) <= 2:
            ret['is_final_pic'] = 0
            ret['inter_dict_dup_hanzi_final_seq_id'] = self.get_tw_char_seq_id(tw_hanzi)
        else:
            ret['is_final_pic'] = 1
            ret['inter_dict_dup_hanzi_final_path'] = get_pic_url_by_source_pic_name(getenum_source('taiwan'), tw_hanzi)

        return ret


class InterDictDedupFilter(django_filters.FilterSet):
    """
    异体字拆字过滤器
    """
    inter_dict_dup_hanzi = django_filters.CharFilter(name=["inter_dict_dup_hanzi_draft", "inter_dict_dup_hanzi_review", "inter_dict_dup_hanzi_final"], method=fields_or_filter_method)
    u_t = django_filters.DateTimeFromToRangeFilter()

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
    if draft.task_status == getenum_task_status("ongoing"):
        draft.task_status = getenum_task_status("completed")
        draft.completed_at = timezone.now()
        review.task_status = getenum_task_status("to_be_arranged")
        variants_dedup.save()
        draft.save()
        review.save()
    elif review.task_status == getenum_task_status("ongoing"):
        review.task_status = getenum_task_status("completed")
        review.completed_at = timezone.now()
        final.task_status = getenum_task_status("to_be_arranged")
        variants_dedup.is_draft_equals_review = variants_dedup.inter_dict_dup_hanzi_draft is variants_dedup.inter_dict_dup_hanzi_review
        variants_dedup.save()
        review.save()
        final.save()
        origin_task = review
    elif final.task_status == getenum_task_status("ongoing"):
        final.task_status = getenum_task_status("completed")
        final.completed_at = timezone.now()
        variants_dedup.is_review_equals_final = variants_dedup.inter_dict_dup_hanzi_review is variants_dedup.inter_dict_dup_hanzi_final
        variants_dedup.save()
        final.save()
        origin_task = final
    else:
        pass
    return origin_task


class InterDictDedupViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsBusinessMember)

    queryset = InterDictDedup.objects.all()
    filter_class = InterDictDedupFilter
    pagination_class = NumberPagination
    serializer_class = InterDictDedupSerializer

    # 提交 此处提交为单个字提交,非页面提交
    @detail_route(methods=["PUT", "GET", "PATCH"])
    def submit_single_variant(self, request, *args, **kwargs):
        variants_dedup = self.get_object()
        serializer = InterDictDedupSerializer(data=request.data)
        task_pacakge_id = serializer.initial_data['task_package_id']
        business_stage = serializer.initial_data['business_stage']
        if serializer.is_valid():
            tasks = list(variants_dedup.task.filter(business_stage=business_stage))
            if not tasks:
                new_task_data = {
                    'user': request.user,
                    'task_package': task_pacakge_id,
                    'content': variants_dedup
                }
                business_stage = create_task(new_task_data)

            if business_stage is getenum_business_stage('init'):
                key = 'inter_dict_dup_hanzi_draft'
            elif business_stage is getenum_business_stage('review'):
                key = 'inter_dict_dup_hanzi_review'
            else:
                key = 'inter_dict_dup_hanzi_final'
            setattr(variants_dedup, key, serializer.initial_data.get('inter_dict_dup_hanzi', getattr(variants_dedup, key)))
            variants_dedup.save()
            serializer = self.serializer_class(variants_dedup)
            return Response(serializer.data)
        else:
            return Response(_("Inputdata Error!"))
