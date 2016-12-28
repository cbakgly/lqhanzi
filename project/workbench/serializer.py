# -*- coding:utf8 -*-
from models import Diaries, Credits
from models import Tag
from rest_framework import serializers


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diaries
        fields = ("user", "tag", "work_types", "work_brief", "content", "c_t", "u_t")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("tag",)


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credits
        fields = ('user', 'credit', 'sort')
