# -*- coding:utf8 -*-
from models import Diary
from models import Tag
from rest_framework import serializers


class DiarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Diary
        fields = ("user_id", "tag", "work_types", "work_brief", "content", "c_t", "u_t")


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ("tag",)
