# -*- coding:utf8 -*-
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters

from ..pagination import NumberPagination
from ..models import VariantsInput, Tasks
from .api_redeem import RedeemSerializer


class VariantsInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantsInput
        fields = "__all__"
        depth = 2


class VariantsInputFilter(django_filters.FilterSet):
    """
    异体字拆字过滤器
    """

    class Meta:
        model = VariantsInput
        fields = ("__all__")


class VariantsInputViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = VariantsInput.objects.all()
    filter_class = VariantsInputFilter
    pagination_class = NumberPagination
    serializer_class = VariantsInputSerializer
