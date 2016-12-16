# -*- coding:utf8 -*-
from models import Diaries
from models import Tag
from rest_framework import serializers


class DiarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Diaries
        fields = ("user_id", "tag", "work_types", "work_brief", "content", "c_t", "u_t")


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ("tag",)
