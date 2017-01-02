# encoding: utf-8
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import rest_framework_filters as drf_filters
import django_filters as filters
from ..models import Tasks
from api_variants_split import VariantsSplitSerializer


# Task Packages management
class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'

    def create(self, validated_data):
        task = Tasks.objects.create(**validated_data)
        task.save()
        return task

    def update(self, instance, validated_data):
        for key in ['business_id', 'business_type', 'user', 'business_stage', 'task_status', 'credits', 'remark', 'completed_at', 'task_package']:
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


class TasksFilter(drf_filters.FilterSet):
    assigned_at = drf_filters.DateFromToRangeFilter()
    completed_at = filters.DateFromToRangeFilter()
    c_t = filters.DateFromToRangeFilter()
    u_t = filters.DateFromToRangeFilter()

    class Meta:
        model = Tasks
        fields = ['variant_split__hanzi_char']


class TasksViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    filter_backends = (filters.rest_framework.DjangoFilterBackend,)
    serializer_class = TasksSerializer
    filter_class = TasksFilter
    queryset = Tasks.objects.all()

    @list_route()
    def split_tasks(self, request, *args, **kwargs):
        split_task = Tasks(pk=1).split_task.all()
        serializer = VariantsSplitSerializer(split_task, many=True)

        return Response(serializer.data)
