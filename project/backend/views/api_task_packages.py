# encoding: utf-8
from __future__ import unicode_literals

import django_filters
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from api_tasks import TasksSerializer
from backend.enums import getenum_business_status
from backend.filters import NumberInFilter
from ..models import TaskPackages, Tasks


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
        user_id = validated_data['user'].id
        biz_type = validated_data['business_type']
        exist = TaskPackages.objects.filter(user_id=user_id).filter(business_type=biz_type).filter(status=getenum_business_status('ongoing'))
        if exist:
            raise ValidationError(_("Only one package per type per stage can it be created."))
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

    def to_representation(self, instance):
        ret = super(TaskPackagesSerializer, self).to_representation(instance)
        ret['business_type_display'] = instance.get_business_type_display()
        ret['business_stage_display'] = instance.get_business_stage_display()
        return ret


class TaskPackagesFilter(django_filters.FilterSet):
    c_t = django_filters.DateFromToRangeFilter()
    completed_at = django_filters.DateFromToRangeFilter()
    business_type_in = NumberInFilter(name='business_type', lookup_expr='in')
    ordering = django_filters.OrderingFilter(fields=('id',))

    class Meta:
        model = TaskPackages
        fields = ["user_id",
                  "business_type",
                  "business_type_in",
                  'c_t',
                  'completed_at',
                  'status', ]


class TaskPackagesViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = TaskPackagesSerializer
    filter_class = TaskPackagesFilter

    def get_queryset(self):
        user = self.request.user
        # TODO: will return object basing on user's group(role)
        if user.is_superuser == 1:
            return TaskPackages.objects.all()
        return TaskPackages.objects.filter(user_id=self.request.user.id)
