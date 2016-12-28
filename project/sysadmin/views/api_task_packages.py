# encoding: utf-8
from __future__ import unicode_literals
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import serializers
import rest_framework_filters as filters

from workbench.models import TaskPackages, Tasks
from api_tasks import TasksSerializer


# Task Packages management
class TaskPackagesSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField('get_today_tasks')

    class Meta:
        model = TaskPackages
        fields = ('id', 'user', 'business_type', 'business_stage', 'size', 'status', 'daily_plan', 'due_date',
                  'completed_num', 'completed_at', 'c_t', 'u_t', 'tasks')

    def get_today_tasks(self, task_package):
        tasks = Tasks.objects.filter(completed_at__gte=timezone.now().date(), task_package=task_package)
        serializer = TasksSerializer(instance=tasks, many=True)
        return serializer.data

    def create(self, validated_data):
        task_package = TaskPackages.objects.create(**validated_data)
        task_package.save()
        return task_package

    def update(self, instance, validated_data):
        for key in ('user', 'business_type', 'business_stage', 'size', 'status', 'daily_plan',
                    'due_date', 'completed_num', 'completed_at', 'c_t', 'u_t'):
            if validated_data.get(key) is not None:
                setattr(instance, key, validated_data.get(key, getattr(instance, key)))

        instance.save()
        return instance


class TaskPackagesFilter(filters.FilterSet):
    c_t = filters.DateFromToRangeFilter()
    completed_at = filters.DateFromToRangeFilter()

    class Meta:
        model = TaskPackages
        fields = '__all__'


class TaskPackagesViewSet(viewsets.ModelViewSet):
    serializer_class = TaskPackagesSerializer
    filter_class = TaskPackagesFilter
    queryset = TaskPackages.objects.all()
