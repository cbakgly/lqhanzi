# -*- coding:utf8 -*-
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
import django_filters

from ..pagination import StandardPagination
from ..serializer import DiarySerializer, CreditSerializer, RedeemSerializer, RedeemSerializerVersion1

from .. import wb_filter
from ..models import Diaries, Credits, CreditsRedeem
from ..versioning import AllVersioning


class DiaryViewSet(viewsets.ModelViewSet):
    """
    允许查看打卡记录的API endpoint
    """
    queryset = Diaries.objects.all()
    serializer_class = DiarySerializer
    filter_class = wb_filter.DiaryFilter
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)


class CreditViewSet(viewsets.ModelViewSet):
    """
    积分
    """
    queryset = Credits.objects.all()
    serializer_class = CreditSerializer
    filter_class = wb_filter.CreditFilter
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    pagination_class = StandardPagination
    versioning_class = AllVersioning

    @list_route()
    def certain_user_credits(self, request):
        user = request.user
        user_credits = user.user_credits.all()
        serializer = CreditSerializer(user_credits, many=True)

        return Response(serializer.data)


def index(request):
    return render(request, 'index.html')


class RedeemViewSet(viewsets.ModelViewSet):
    """
    积分兑换
    """
    queryset = CreditsRedeem.objects.all()
    versioning_class = AllVersioning
    filter_class = wb_filter.RedeemFilter
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    pagination_class = StandardPagination

    def get_serializer_class(self):
        if self.request.version == "v1":
            return RedeemSerializer
        else:
            return RedeemSerializerVersion1
