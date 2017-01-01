# encoding: utf-8
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now, timedelta

import django_filters.rest_framework
import rest_framework_filters as drf_filters
import datetime

from backend.models import Diaries, User
from backend.pagination import NumberPagination


# Operation log management
class DiariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diaries
        fields = '__all__'

    def create(self, validated_data):
        diary = Diaries.objects.create(**validated_data)
        return diary

    def update(self, instance, validated_data):
        return instance

    def to_representation(self, instance):
        ret = super(DiariesSerializer, self).to_representation(instance)
        ret['tag_choices_display'] = instance.get_tag_choices_display()
        return ret


class DiariesFilter(drf_filters.FilterSet):
    c_t = drf_filters.DateFromToRangeFilter()
    u_t = drf_filters.DateFromToRangeFilter()

    class Meta:
        model = Diaries
        fields = '__all__'


class DiariesViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = DiariesSerializer
    filter_class = DiariesFilter
    queryset = Diaries.objects.all()


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diaries
        fields = ("__all__")

    def create(self, validated_data):
        user = self.context['request'].user
        start = now().date()
        end = start + timedelta(days=1)
        today_tasks = user.user_task.all().filter(completed_at__range=(start, end))
        work_summary = {
            0: 0,
            1: 0,
            2: 0
        }
        work_types = ""
        work_brief = ""
        for t in today_tasks:
            if t.business_type == 0:
                work_summary[0] += 1
            elif t.business_type == 1:
                work_summary[1] += 1
            else:
                work_summary[2] += 1

        business_types = ["录入", "去重", "拆字"]

        for i, item in enumerate(business_types):
            if work_summary[i] != 0:
                work_types += item + ""
                work_brief += item + str(work_summary[i]) + "个 "

        diary = Diaries(user=User(id=user.id), tag=validated_data['tag'],
                        work_brief=work_brief, work_types=work_types,
                        content=validated_data['content'],
                        c_t=datetime.datetime.now(),
                        u_t=datetime.datetime.now())
        diary.save()
        return diary

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.work_types = validated_data.get('work_types', instance.work_types)
        instance.work_brief = validated_data.get('work_brief', instance.work_brief)
        instance.content = validated_data.get('content', instance.content)
        instance.u_t = datetime.datetime.now()
        instance.save()
        return instance


class DiaryFilter(drf_filters.FilterSet):
    """
    根据用户id和时间来筛选
    """
    c_t = drf_filters.DateFromToRangeFilter()

    class Meta:
        model = Diaries
        fields = ["user__username", "c_t"]


class DiaryViewSet(viewsets.ModelViewSet):
    """
    允许查看打卡记录的API endpoint
    """
    queryset = Diaries.objects.all()
    serializer_class = DiarySerializer
    filter_class = DiaryFilter
    pagination_class = NumberPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    ordering = ('c_t')
