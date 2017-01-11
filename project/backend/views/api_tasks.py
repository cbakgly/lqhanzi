# encoding: utf-8
from __future__ import unicode_literals
from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters

from ..pagination import NumberPagination
from ..models import Tasks, VariantsSplit, VariantsInput, KoreanDedup, InterDictDedup
from ..enums import getenum_business_type
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
        elif isinstance(task_ele, KoreanDedup) or isinstance(task_ele, InterDictDedup):
            ele_serializer = api_variants_dedup
        else:
            pass
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

    def retrieve_task(self, user, business_type, business_stage):
        if user.is_superuser == 1:
            queryset = Tasks.objects.filter(business_type=business_type).filter(business_stage=business_stage)
        else:
            queryset = Tasks.objects.filter(user_id=user.id).filter(business_type=business_type).filter(business_stage=business_stage)
        serializer = self.serializer_class(queryset, many=True)

    @list_route()
    def split(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser == 1:
            queryset = Tasks.objects.filter(business_type=getenum_business_type('split'))
        else:
            queryset = Tasks.objects.filter(user_id=user.id).filter(business_type=getenum_business_type('split'))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @list_route()
    def input(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser == 1:
            queryset = Tasks.objects.filter(business_type=getenum_business_type('input'))
        else:
            queryset = Tasks.objects.filter(user_id=user.id).filter(business_type=getenum_business_type('input'))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @list_route()
    def dedup(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser == 1:
            queryset = Tasks.objects.filter(business_type=getenum_business_type('dedup'))
        else:
            queryset = Tasks.objects.filter(user_id=user.id).filter(business_type=getenum_business_type('dedup'))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    # 太难跳过，仅拆字
    @detail_route(methods=["PATCH", "GET", "PUT"])
    def skip_task(self, request, *args, **kwargs):
        origin_task = self.get_object()
        work_ele = origin_task.content_object

        business_type = origin_task.business_type
        business_stage = origin_task.business_stage
        user = origin_task.user
        task_package = origin_task.task_package

        if business_stage is 0:
            work_ele.skip_num_draft += 1
        elif business_stage is 1:
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
