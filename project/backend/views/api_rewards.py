# -*- coding:utf8 -*-
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework import viewsets
from rest_framework import serializers

import django_filters

from ..pagination import NumberPagination
from ..models import Reward
from ..auth import IsBusinessMember


class RewardFilter(django_filters.FilterSet):
    """
    根据用户来获取
    """
    class Meta:
        model = Reward
        fields = "__all__"


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = "__all__"


class RewardSerializerVersion1(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = "__all__"
        depth = 1


class RewardViewSet(viewsets.ModelViewSet):
    """
    积分兑换
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsBusinessMember)

    queryset = Reward.objects.all()
    filter_class = RewardFilter
    pagination_class = NumberPagination
    serializer_class = RewardSerializer
