# encoding: utf-8

from __future__ import unicode_literals
from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters
# from django.db.models import Q

from ..pagination import NumberPagination
from ..models import Tasks, VariantsSplit, VariantsInput, KoreanDedup
from ..enums import getenum_business_type, getenum_business_status, getenum_business_stage
import api_variants_input
import api_variants_dedup
import api_variants_split
from task_func import assign_task


def reset_task(task):
    task.task_package = None
    task.assigned_at = None
    task.user = None
    task.task_status = 0
    task.save()

    return task


# Task Packages management
class TasksSerializer(serializers.ModelSerializer):
    task_ele = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = "__all__"

    def create(self, validated_data):
        task = Tasks.objects.create(**validated_data)
        task.save()
        return task

    def update(self, instance, validated_data):
        for key in ['business_id', 'business_type', 'user', 'business_stage', 'task_status',
                    'credits', 'remark', 'completed_at', 'task_package']:
            if validated_data.get(key) is not None:  # Only Set values which is put.
                setattr(instance, key, validated_data.get(key, getattr(instance, key)))

            instance.save()

        return instance

    def to_representation(self, instance):
        ret = super(TasksSerializer, self).to_representation(instance)
        ret['business_type_display'] = instance.get_business_type_display()
        ret['business_stage_display'] = instance.get_business_stage_display()
        ret['task_status_display'] = instance.get_task_status_display()
        return ret

    def get_task_ele(self, obj):
        task_ele = obj.content_object
        if isinstance(task_ele, VariantsInput):
            ele_serializer = api_variants_input.VariantsInputSerializer
        elif isinstance(task_ele, VariantsSplit):
            ele_serializer = api_variants_split.VariantsSplitSerializer
        elif isinstance(task_ele, KoreanDedup):
            ele_serializer = api_variants_dedup.KoreanDedupSerializer
        else:
            ele_serializer = api_variants_dedup.InterDictDedupSerializer

        serialized_data = ele_serializer(task_ele).data
        return serialized_data


class TasksFilter(django_filters.FilterSet):
    assigned_at = django_filters.DateFromToRangeFilter()
    completed_at = django_filters.DateFromToRangeFilter()
    ordering = django_filters.OrderingFilter(fields=('id',))

    class Meta:
        model = Tasks
        fields = "__all__"


class TasksViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    pagination_class = NumberPagination
    serializer_class = TasksSerializer
    filter_class = TasksFilter
    queryset = Tasks.objects.all()

    # 拆字
    @list_route()
    def ongoing_split(self, request, *args, **kwargs):
        user = self.request.user
        source = self.request.query_params["source"]
        hanzi_char = self.request.query_params["hanzi_char"]
        similar_parts = self.request.query_params["similar_parts"]
        task_package = request.query_params["task_package"]
        business_type = getenum_business_type("split")
        if user.is_superuser == 1:
            tasks = Tasks.objects.filter(business_type=business_type).filter(task_status=getenum_business_status("ongoing")).filter(task_package=task_package)
        else:
            tasks = Tasks.objects.filter(user_id=user.id).filter(business_type=business_type).filter(task_status=getenum_business_status("ongoing")).filter(task_package=task_package)

        serializer = self.serializer_class(tasks, many=True)
        split_variants = [v["task_ele"] for v in serializer.data]
        business_stage = serializer.data[0]["business_stage"]
        if business_stage == getenum_business_stage("init"):
            similar_parts_comp = "similar_parts_draft"
        elif business_stage == getenum_business_stage("review"):
            similar_parts_comp = "similar_parts_review"
        else:
            similar_parts_comp = "similar_parts_final"
        results = []
        staged_result = []
        key_list = {
            1: [
                "id",
                "task_package",
                'skip_num_draft',
                'init_split_draft',
                'other_init_split_draft',
                'deform_split_draft',
                'similar_parts_draft',
                'dup_id_draft'
            ],
            2: [
                "id",
                "task_package",
                'skip_num_review',
                'init_split_review',
                'other_init_split_review',
                'deform_split_review',
                'similar_parts_review',
                'dup_id_review'
            ],
            3: [
                "id",
                "task_package",
                'skip_num_final',
                'init_split_final',
                'other_init_split_final',
                'deform_split_final',
                'similar_parts_final',
                'dup_id_final'
            ]
        }

        for split_variant in split_variants:
            if split_variant["source"] == int(source) \
                    or hanzi_char in split_variant["hanzi_char"] \
                    or similar_parts in split_variant[similar_parts_comp]:
                split_variant["task_package"] = int(task_package)
                results.append(split_variant)
        for result in results:
            tmp = {}
            for key in key_list[business_stage]:
                tmp[key] = result[key]
            staged_result.append(tmp)
        return Response({"model": staged_result})

    @list_route()
    def ongoing_input(self, request, *args, **kwargs):
        user = self.request.user
        page_num = self.request.query_params["page_num"]
        hanzi_char = self.request.query_params["hanzi_char"]
        note = self.request.query_params["note"]
        variant_type = self.request.query_params["variant_type"]
        task_package = request.query_params["task_package"]
        business_type = getenum_business_type("input")
        if user.is_superuser == 1:
            tasks = Tasks.objects.filter(business_type=business_type).filter(task_status=getenum_business_status("ongoing")).filter(task_package=task_package)
        else:
            tasks = Tasks.objects.filter(user_id=user.id).filter(business_type=business_type).filter(task_status=getenum_business_status("ongoing")).filter(task_package=task_package)

        serializer = self.serializer_class(tasks, many=True)
        input_variants = [v["task_ele"] for v in serializer.data]
        business_stage = serializer.data[0]["business_stage"]
        if business_stage == getenum_business_stage("init"):
            hanzi_char_comp = "hanzi_char_draft"
            variant_type_comp = 'variant_type_draft'
        elif business_stage == getenum_business_stage("review"):
            hanzi_char_comp = "hanzi_char_review"
            variant_type_comp = 'variant_type_review'
        else:
            hanzi_char_comp = "hanzi_char_final"
            variant_type_comp = 'variant_type_final'
        results = []
        staged_result = []
        key_list = {
            1: [
                "id",
                "task_package",
                'page_num',
                'seq_num_draft',
                'hanzi_char_draft',
                'hanzi_pic_id_draft',
                'variant_type_draft',
                'std_hanzi_draft',
                'notes_draft',
                'is_del_draft'
            ],
            2: [
                "id",
                "task_package",
                'page_num',
                'seq_num_review',
                'hanzi_char_review',
                'hanzi_pic_id_review',
                'variant_type_review',
                'std_hanzi_review',
                'notes_review',
                'is_del_review'
            ],
            3: [
                "id",
                "task_package",
                'page_num',
                'seq_num_final',
                'hanzi_char_final',
                'hanzi_pic_id_final',
                'variant_type_final',
                'std_hanzi_final',
                'notes_final',
                'is_del_final'
            ]
        }

        for input_variant in input_variants:
            if input_variant["page_num"] == int(page_num) \
                    or hanzi_char in input_variant[hanzi_char_comp] \
                    or note in input_variant[note]\
                    and variant_type == input_variant[variant_type_comp]:
                input_variant["task_package"] = int(task_package)
                results.append(input_variant)
        for result in results:
            tmp = {}
            for key in key_list[business_stage]:
                tmp[key] = result[key]
            staged_result.append(tmp)
        return Response({"results": staged_result})


'''
# 录入
@list_route()
def input(self, request, *args, **kwargs):
    serializer = retrieve_task(request, "input")
    return Response(serializer.data)


# 去重
@list_route()
def dedup(self, request, *args, **kwargs):
    serializer = retrieve_task(request, "dedup")
    return Response(serializer.data)
'''


# 太难跳过，仅拆字
@detail_route(methods=["PATCH", "GET", "PUT"])
def skip_task(self, request, *args, **kwargs):
    origin_task = self.get_object()
    work_ele = origin_task.content_object

    business_type = origin_task.business_type
    business_stage = origin_task.business_stage
    user = origin_task.user
    task_package = origin_task.task_package

    if business_stage == getenum_business_stage("init"):
        work_ele.skip_num_draft += 1
    elif business_stage == getenum_business_stage("review"):
        work_ele.skip_num_review += 1
    else:
        work_ele.skip_num_final += 1
    work_ele.save()
    reset_task(origin_task)

    new_task = assign_task(business_type, business_stage, task_package, user)
    if new_task:
        serializer = api_variants_split.VariantsSplitSerializer(new_task.content_object)
        return Response(serializer.data)
    else:
        return Response(u"没有更多任务了，明天再来吧！", status=status.HTTP_204_NO_CONTENT)
