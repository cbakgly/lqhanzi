# -*- coding:utf8 -*-
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.template import Context
import django_filters.rest_framework

from ..pagination import SmallResultsSetPagination
from ..serializer import DiarySerializer, TagSerializer, CreditSerializer
from .. import wb_filter
from ..models import Diaries, Tag, Credits
from .credits import get_user_today_and_total_credits


class DiaryViewSet(viewsets.ModelViewSet):
    """
    允许查看打卡记录的API endpoint
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Diaries.objects.all()
    serializer_class = DiarySerializer
    filter_class = wb_filter.DiaryFilter
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class TagViewSet(viewsets.ModelViewSet):
    """
    允许查看打卡类型的API endpoint
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CreditViewSet(viewsets.ModelViewSet):
    """
    积分
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Credits.objects.all()
    serializer_class = CreditSerializer
    filter_class = wb_filter.CreditFilter
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    pagination_class = SmallResultsSetPagination


@login_required
def index(request):
    c = Context()
    c.update(get_user_today_and_total_credits(request.user.id))
    return render(request, 'diaries.html', c)
