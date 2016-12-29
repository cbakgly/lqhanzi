# -*- coding:utf8 -*-
import datetime

from rest_framework import serializers

from models import Diaries, Credits, CreditsRedeem
from sysadmin.models import User


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diaries
        fields = ("__all__")

    def create(self, validated_data):
        user = self.context['request'].user
        diary = Diaries(user=User(id=user.id), tag=validated_data['tag'],
                        work_types=validated_data['work_types'],
                        work_brief=validated_data['work_brief'],
                        content=validated_data['content'],
                        c_t=datetime.datetime.now(),
                        u_t=datetime.datetime.now())
        diary.save()
        return Diaries(**validated_data)

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
        depth = 1

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
