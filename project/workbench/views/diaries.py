# -*- coding:utf8 -*-
from .. import models
from rest_framework import viewsets
from .. import filter
from rest_framework import filters
from django.shortcuts import render
from rest_framework.views import APIView

from .. import serializer


class DiaryViewSet(viewsets.ModelViewSet):
    """
    允许查看打卡记录的API endpoint
    """
    queryset = models.Diary.objects.all()
    serializer_class = serializer.DiarySerializer
    filter_class = filter.DiaryFilter
    ordering_fields = ('c_t')


class TagViewSet(viewsets.ModelViewSet):
    """
    允许查看打卡类型的API endpoint
    """
    queryset = models.Tag.objects.all()
    serializer_class = serializer.TagSerializer

