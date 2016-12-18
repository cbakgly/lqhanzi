# -*- coding:utf8 -*-
from rest_framework import viewsets
import django_filters

from ..pagination import SmallResultsSetPagination
from ..serializer import DiarySerializer, TagSerializer, CreditSerializer
from .. import wb_filter
from ..models import Diaries, Tag, Credits


class DiaryViewSet(viewsets.ModelViewSet):
    """
    允许查看打卡记录的API endpoint
    """
    queryset = Diaries.objects.all()
    serializer_class = DiarySerializer
    filter_class = wb_filter.DiaryFilter
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class TagViewSet(viewsets.ModelViewSet):
    """
    允许查看打卡类型的API endpoint
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CreditViewSet(viewsets.ModelViewSet):
    """
    积分
    """
    queryset = Credits.objects.all()
    serializer_class = CreditSerializer
    filter_class = wb_filter.CreditFilter
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    pagination_class = SmallResultsSetPagination
