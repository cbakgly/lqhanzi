# -*- coding:utf8 -*-
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
import django_filters

from ..pagination import NumberPagination
from ..serializer import DiarySerializer, CreditSerializer, RedeemSerializer, VariantsSplitSerializer

from .. import wb_filter
from ..models import Diaries, Credits, CreditsRedeem, VariantsSplit, Tasks
from ..versioning import AllVersioning


class DiaryViewSet(viewsets.ModelViewSet):
    """
    允许查看打卡记录的API endpoint
    """
    queryset = Diaries.objects.all()
    serializer_class = DiarySerializer
    filter_class = wb_filter.DiaryFilter
    pagination_class = NumberPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

class CreditViewSet(viewsets.ModelViewSet):
    """
    积分
    """
    queryset = Credits.objects.all()
    serializer_class = CreditSerializer
    filter_class = wb_filter.CreditFilter
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    pagination_class = NumberPagination
    versioning_class = AllVersioning


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
    pagination_class = NumberPagination
    serializer_class = RedeemSerializer

    '''def get_serializer_class(self):
        if self.request.version == "v1":
            return RedeemSerializer
        else:
            return RedeemSerializerVersion1'''

    @list_route()
    def certain_user_redeem(self, request):
        user = request.user
        user_credits = user.applier.all()
        serializer = RedeemSerializer(user_credits, many=True)

        return Response(serializer.data)


class VariantsSplitViewSet(viewsets.ModelViewSet):
    queryset = VariantsSplit.objects.all()
    versioning_class = AllVersioning
    filter_class = wb_filter.VariantsSplitFilter
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    pagination_class = NumberPagination
    serializer_class = VariantsSplitSerializer

    '''def get_serializer_class(self):
        if self.request.version == "v1":
            return RedeemSerializer
        else:
            return RedeemSerializerVersion1'''

    @list_route()
    def some_split_tasks(self, request):
        tasks = Tasks.objects.filter(business_type=2)
        split_tasks = tasks.split_task.all()
        serializer = RedeemSerializer(split_tasks, many=True)

        return Response(serializer.data)
