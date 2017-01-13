# -*- coding:utf8 -*-
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route
import django_filters

from ..pagination import NumberPagination
from ..models import VariantsSplit
from task_func import assign_task
from ..enums import getenum_business_status


class VariantsSplitSerializer(serializers.ModelSerializer):
    task = serializers.SerializerMethodField()

    class Meta:
        model = VariantsSplit
        # fields = ["split_task"]
        fields = ['source',
                  'hanzi_type',
                  'hanzi_char',
                  'hanzi_pic_id',
                  'variant_type',
                  'std_hanzi',
                  'as_std_hanzi',
                  'seq_id',
                  'is_redundant',
                  'skip_num_draft',
                  'init_split_draft',
                  'other_init_split_draft',
                  'deform_split_draft',
                  'similar_parts_draft',
                  'dup_id_draft',
                  'skip_num_review',
                  'init_split_review',
                  'other_init_split_review',
                  'deform_split_review',
                  'similar_parts_review',
                  'dup_id_review',
                  'skip_num_final',
                  'init_split_final',
                  'other_init_split_final',
                  'deform_split_final',
                  'similar_parts_final',
                  'dup_id_final',
                  'is_draft_equals_review',
                  'is_review_equals_final',
                  'is_checked',
                  'is_submitted',
                  'remark',
                  'c_t',
                  'u_t',
                  'task'
                  ]

    def get_task(self, obj):
        tasks = list(obj.task.all())
        task_dic = {}
        for t in tasks:
            task_dic[t.business_stage] = t.id
        return task_dic


class VariantsSplitFilter(django_filters.FilterSet):

    """
    异体字拆字过滤器
    """

    class Meta:
        model = VariantsSplit
        fields = ("__all__")


def update_tasks_status(variants_split):
    tasks = list(variants_split.task.all())
    task_dict = {}
    for t in tasks:
        task_dict[t.business_stage] = t
    draft = task_dict[0]
    review = task_dict[1]
    final = task_dict[2]
    origin_task = draft
    if draft.task_status == getenum_business_status("ongoing"):
        draft.task_status = getenum_business_status("completed")
        draft.completed_at = timezone.now()
        review.task_status = getenum_business_status("to_be_arranged")
        variants_split.save()
        draft.save()
        review.save()
    elif review.task_status == getenum_business_status("ongoing"):
        review.task_status = getenum_business_status("completed")
        review.completed_at = timezone.now()
        final.task_status = getenum_business_status("to_be_arranged")
        variants_split.is_draft_equals_review = variants_split.init_split_draft is variants_split.init_split_review
        variants_split.save()
        review.save()
        final.save()
        origin_task = review
    elif final.task_status == getenum_business_status("ongoing"):
        final.task_status = getenum_business_status("completed")
        final.completed_at = timezone.now()
        variants_split.is_review_equals_final = variants_split.init_split_final is variants_split.init_split_review
        variants_split.save()
        final.save()
        origin_task = final
    else:
        pass
    return origin_task


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
                    return Response(u"没有更多任务了！", status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(u"该任务包已完成，请领取新任务包。", status=status.HTTP_100_CONTINUE)
        return Response("数据错误！")

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
            return Response("数据错误！")
