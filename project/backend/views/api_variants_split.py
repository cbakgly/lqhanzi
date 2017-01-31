# -*- coding:utf8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
import django_filters

from ..pagination import NumberPagination
from ..models import VariantsSplit
from task_func import assign_task
from ..enums import getenum_task_status, getenum_business_stage
from ..utils import get_pic_url_by_source_pic_name
from ..filters import fields_or_filter_method


class VariantsSplitSerializer(serializers.ModelSerializer):
    task = serializers.SerializerMethodField()

    class Meta:
        model = VariantsSplit
        # fields = ["split_task"]
        fields = "__all__"

    def get_task(self, obj):
        tasks = list(obj.task.all())
        task_dic = {}
        for t in tasks:
            task_dic[t.business_stage] = t.id
        return task_dic

    def to_representation(self, instance):
        ret = super(VariantsSplitSerializer, self).to_representation(instance)
        ret['hanzi_pic_path'] = get_pic_url_by_source_pic_name(ret['source'], ret['hanzi_pic_id'])
        ret['variant_type_display'] = instance.get_variant_type_display()
        ret['hanzi_type_display'] = instance.get_hanzi_type_display()
        ret['source_display'] = instance.get_source_display()
        ret['is_draft_equals_review_display'] = instance.get_is_draft_equals_review_display()
        ret['is_review_equals_final_display'] = instance.get_is_review_equals_final_display()
        ret['is_checked_display'] = instance.get_is_checked_display()
        ret['is_submitted_display'] = instance.get_is_submitted_display()
        return ret


class VariantsSplitFilter(django_filters.FilterSet):

    """
    异体字拆字过滤器
    """
    u_t = django_filters.DateTimeFromToRangeFilter()
    split = django_filters.CharFilter(name=["init_split_draft", "other_init_split_draft", "deform_split_draft",
                                            "init_split_review", "other_init_split_review", "deform_split_review",
                                            "init_split_final", "other_init_split_final", "deform_split_final"], method=fields_or_filter_method)
    split_draft = django_filters.CharFilter(name=["init_split_draft", "other_init_split_draft", "deform_split_draft"], method=fields_or_filter_method)
    split_review = django_filters.CharFilter(name=["init_split_review", "other_init_split_review", "deform_split_review"], method=fields_or_filter_method)
    split_final = django_filters.CharFilter(name=["init_split_final", "other_init_split_final", "deform_split_final"], method=fields_or_filter_method)
    similar_parts = django_filters.CharFilter(name=["similar_parts_draft", "similar_parts_review", "similar_parts_final"], method=fields_or_filter_method)
    dup_id = django_filters.CharFilter(name=["dup_id_draft", "dup_id_review", "dup_id_final"], method=fields_or_filter_method)
    skip_num = django_filters.CharFilter(name=["skip_num_draft", "skip_num_review", "skip_num_final"], method=fields_or_filter_method)

    class Meta:
        model = VariantsSplit
        fields = "__all__"


def update_tasks_status(variants_split):
    tasks = list(variants_split.task.all())
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
        variants_split.save()
        draft.save()
        review.save()
    elif review.task_status == getenum_task_status("ongoing"):
        review.task_status = getenum_task_status("completed")
        review.completed_at = timezone.now()
        final.task_status = getenum_task_status("to_be_arranged")
        variants_split.is_draft_equals_review = variants_split.init_split_draft is variants_split.init_split_review
        variants_split.save()
        review.save()
        final.save()
        origin_task = review
    elif final.task_status == getenum_task_status("ongoing"):
        final.task_status = getenum_task_status("completed")
        final.completed_at = timezone.now()
        variants_split.is_review_equals_final = variants_split.init_split_final is variants_split.init_split_review
        variants_split.save()
        final.save()
        origin_task = final
    else:
        pass
    return origin_task


class SingleSerializer(serializers.ModelSerializer):

    class Meta:
        model = VariantsSplit
        fields = "__all__"


class VariantsSplitViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = VariantsSplit.objects.all()
    filter_class = VariantsSplitFilter
    pagination_class = NumberPagination
    serializer_class = VariantsSplitSerializer

    # 提交并转下一条
    @detail_route(methods=["PUT", "GET", "PATCH"])
    def submit_and_next(self, request, *args, **kwargs):
        variants_split = self.get_object()
        serializer = VariantsSplitSerializer(data=request.data)

        if serializer.is_valid():
            origin_task = update_tasks_status(variants_split)

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
                    return Response(_("No more task today, have a try tommorrow!"), status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(_("This package is completed, please apply for a new one!"), status=status.HTTP_100_CONTINUE)
        return Response(_("Inputdata Error!"))

    # 提交
    @detail_route(methods=["PUT", "GET", "PATCH"])
    def submit(self, request, *args, **kwargs):
        variants_split = self.get_object()
        serializer = VariantsSplitSerializer(data=request.data)

        if serializer.is_valid():
            origin_task = update_tasks_status(variants_split)
            task_ele = origin_task.content_object
            for key in serializer.initial_data.keys():
                setattr(task_ele, key, serializer.initial_data.get(key, getattr(task_ele, key)))
            task_ele.save()
            serializer = self.serializer_class(task_ele)
            return Response(serializer.data)
        else:
            return Response(_("Inputdata Error!"))

    @list_route(methods=["GET"])
    def single_split(self, request, *args, **kwargs):
        id = self.request.query_params["id"]
        qs = VariantsSplit.objects.filter(pk=int(id))
        data = list(qs)[0]
        return Response(data)
