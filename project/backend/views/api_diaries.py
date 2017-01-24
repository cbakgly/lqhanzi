# encoding: utf-8
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime
import django_filters

from backend.models import Diaries, BUSINESS_TYPE_CHOICES
from backend.pagination import NumberPagination
from backend.utils import is_int


# Operation log management
class DiariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diaries
        fields = "__all__"

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     start = now().date()
    #     end = start + timedelta(days=1)
    #     today_tasks = user.user_task.all().filter(completed_at__range=(start, end))
    #     work_summary = {
    #         0: 0,
    #         1: 0,
    #         2: 0
    #     }
    #     work_types = ""
    #     work_brief = ""
    #     for t in today_tasks:
    #         if t.business_type == 0:
    #             work_summary[0] += 1
    #         elif t.business_type == 1:
    #             work_summary[1] += 1
    #         else:
    #             work_summary[2] += 1
    #
    #     business_types = ["录入", "去重", "拆字"]
    #
    #     for i, item in enumerate(business_types):
    #         if work_summary[i] != 0:
    #             work_types += item + " "
    #             work_brief += item + str(work_summary[i]) + "个 "
    #
    #     diary = Diaries(user=User(id=user.id), tag=validated_data['tag'],
    #                     work_brief=work_brief, work_types=work_types,
    #                     content=validated_data['content'],
    #                     c_t=timezone.now(),
    #                     u_t=timezone.now())
    #     diary.save()
    #     return diary

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.work_types = validated_data.get('work_types', instance.work_types)
        instance.work_brief = validated_data.get('work_brief', instance.work_brief)
        instance.content = validated_data.get('content', instance.content)
        instance.u_t = timezone.now()
        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super(DiariesSerializer, self).to_representation(instance)
        ret['tag_display'] = instance.get_tag_display()
        ret['work_types'] = dict(BUSINESS_TYPE_CHOICES)[int(ret['work_types'])] if is_int(ret['work_types']) else ret['work_types']
        ret['work_brief'] = ret['work_types'] + ' ' + ret['work_brief'] if is_int(ret['work_brief']) else ret['work_brief']
        return ret

    # TODO: 需要对用户提交的html内容进行安全过滤
    def to_internal_value(self, data):
        new = data.copy()
        new['user'] = self.context['request'].user.id
        new['c_t'] = timezone.now()
        new['u_t'] = timezone.now()

        now = timezone.now()
        start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
        end = start + timezone.timedelta(days=1)
        today_tasks = self.context['request'].user.user_task.all().filter(completed_at__range=(start, end))

        work_types = ""
        work_brief = ""
        if today_tasks:
            work_summary = dict([(key, 0) for key in dict(BUSINESS_TYPE_CHOICES)])
            for t in today_tasks:
                work_summary[int(t.business_type)] += 1

            for i, item in enumerate(BUSINESS_TYPE_CHOICES):
                if work_summary[i] != 0:
                    work_types += item + " "
                    work_brief += item + str(work_summary[i]) + "个 "

        new['work_types'] = work_types
        new['work_brief'] = work_brief

        return super(DiariesSerializer, self).to_internal_value(new)


class DiariesFilter(django_filters.FilterSet):
    """
    根据用户id和时间来筛选
    """
    c_t = django_filters.filters.DateTimeFromToRangeFilter()
    ordering = django_filters.OrderingFilter(fields=('id',))

    class Meta:
        model = Diaries
        fields = '__all__'


class DiariesViewSet(viewsets.ModelViewSet):
    """
    允许查看打卡记录的API endpoint
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Diaries.objects.all()
    serializer_class = DiariesSerializer
    filter_class = DiariesFilter
    pagination_class = NumberPagination

    def get_queryset(self):
        user_id = self.request.user.id
        return Diaries.objects.filter(user_id=user_id)
