# encoding: utf-8
from __future__ import unicode_literals
from sysadmin.models import User
from sysadmin.models import Operation
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.decorators import detail_route, list_route
import rest_framework_filters as filters
from rest_framework.response import Response
from workbench.models import Tasks

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
            if validated_data.get(key) != None: # Only Set values which is put.
                setattr(instance, key, validated_data.get(key, getattr(instance, key)))

            instance.save()

        return instance

class TasksFilter(filters.FilterSet):
    assigned_at = filters.DateFromToRangeFilter()
    completed_at = filters.DateFromToRangeFilter()
    c_t = filters.DateFromToRangeFilter()
    u_t = filters.DateFromToRangeFilter()

    class Meta:
        model = Tasks
        fields = '__all__'

class TasksViewSet(viewsets.ModelViewSet):
    serializer_class = TasksSerializer
    filter_class = TasksFilter
    queryset = Tasks.objects.all()
