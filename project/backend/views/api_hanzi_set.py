# -*- coding:utf8 -*-
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters

from ..pagination import NumberPagination
from ..models import HanziSet


class HanziSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = HanziSet
        fields = "__all__"
        depth = 0


class HanziSetFilter(django_filters.FilterSet):
    """
    异体字拆字过滤器
    """

    class Meta:
        model = HanziSet
        fields = ("__all__")


class HanziSetViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = HanziSet.objects.all()
    filter_class = HanziSetFilter
    pagination_class = NumberPagination
    serializer_class = HanziSetSerializer
