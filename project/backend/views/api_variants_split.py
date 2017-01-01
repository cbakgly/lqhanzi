# -*- coding:utf8 -*-
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from ..pagination import NumberPagination
from ..models import VariantsSplit, Tasks
from .api_redeem import RedeemSerializer


class VariantsSplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantsSplit
        fields = "__all__"
        depth = 2


class VariantsSplitFilter(django_filters.FilterSet):
    """
    异体字拆字过滤器
    """

    class Meta:
        model = VariantsSplit
        fields = ("__all__")


class VariantsSplitViewSet(viewsets.ModelViewSet):
    queryset = VariantsSplit.objects.all()
    filter_class = VariantsSplitFilter
    filter_backends = (DjangoFilterBackend,)
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
