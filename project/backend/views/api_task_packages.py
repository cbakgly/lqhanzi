# encoding: utf-8
from __future__ import unicode_literals

import django_filters
from datetime import datetime
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from api_tasks import TasksSerializer
from task_func import assign_task
from backend.enums import getenum_task_package_business_status
from backend.filters import NumberInFilter
from ..models import TaskPackages, Tasks, BUSINESS_STAGE_CHOICES, BUSINESS_TYPE_CHOICES


# Task Packages management
class TaskPackagesSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField('get_today_tasks')
    credits = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = TaskPackages
        fields = ('id', 'user', 'business_type', 'business_stage', 'size', 'status', 'daily_plan', 'due_date',
                  'completed_num', 'completed_at', 'c_t', 'u_t', 'tasks', 'credits', 'name')

    def get_today_tasks(self, task_package):
        now = timezone.now()
        today = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
        tasks = Tasks.objects.filter(completed_at__gte=today, task_package=task_package)
        serializer = TasksSerializer(instance=tasks, many=True)
        return serializer.data

    def create(self, validated_data):
        user_id = validated_data['user'].id
        biz_type = validated_data['business_type']
        biz_stage = validated_data['business_stage']
        exist = TaskPackages.objects.filter(user_id=user_id).filter(business_type=biz_type).filter(status=getenum_task_package_business_status('ongoing'))
        if exist:
            raise ValidationError(_("Only one task package per type and stage can be created."))

        due_days = validated_data['size'] / validated_data['daily_plan']
        c_t = timezone.now()
        due_date = c_t + timezone.timedelta(days=due_days)
        validated_data['due_date'] = due_date
        validated_data['c_t'] = c_t
        task_package = TaskPackages.objects.create(**validated_data)
        task_package.save()

        # 分配第一个任务
        assign_task(biz_type, biz_stage, task_package, validated_data['user'])
        return task_package

    def update(self, instance, validated_data):
        for key in validated_data.keys():
            if validated_data.get(key) is not None:
                setattr(instance, key, validated_data.get(key, getattr(instance, key)))

        due_days = instance.size / validated_data['daily_plan']
        c_t = timezone.now()
        setattr(instance, "due_date", c_t + timezone.timedelta(days=due_days))
        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super(TaskPackagesSerializer, self).to_representation(instance)
        ret['business_type_display'] = instance.get_business_type_display()
        ret['business_stage_display'] = instance.get_business_stage_display()
        return ret

    def get_credits(self, instance):
        sum_credits = Tasks.objects.filter(task_package=instance).aggregate(Sum("credits"))
        return sum_credits

    def get_name(self, instance):
        return "#" + business_type_choices[instance.business_type - 1][1] + business_stage_choices[instance.business_stage - 1][1] + str(instance.size) + str(instance.id)


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
        else:
            return TaskPackages.objects.filter(user_id=self.request.user.id)
