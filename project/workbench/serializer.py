# -*- coding:utf8 -*-
import datetime
from django.utils.timezone import now, timedelta
from rest_framework import serializers

from models import Diaries, Credits, CreditsRedeem, VariantsSplit
from sysadmin.models import User


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


class CreditSerializer(serializers.ModelSerializer):
    rank = serializers.SerializerMethodField()
    sort = serializers.SerializerMethodField()

    class Meta:
        model = Credits
        fields = ("id", "user", "credit", "sort", "rank")
        depth = 0

    def get_rank(self, obj):
        ranks = {}
        credit_set = Credits.objects.all()
        for i in range(1, 6):
            ranks[i] = []

        for c in credit_set:
            cd = c.credit
            cs = c.sort
            if cd not in ranks[cs]:
                ranks[cs].append(cd)
        for i in range(1, 6):
            ranks[i].sort()
            ranks[i].reverse()
        return ranks[obj.sort].index(obj.credit) + 1

    def get_sort(self, obj):
        for sc in Credits.sort_choices:
            if obj.sort == sc[0]:
                return sc[1]


class RedeemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditsRedeem
        fields = ("__all__")


class RedeemSerializerVersion1(serializers.ModelSerializer):
    class Meta:
        model = CreditsRedeem
        fields = ("__all__")
        depth = 1


class VariantsSplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantsSplit
        fields = "__all__"
        depth = 2
