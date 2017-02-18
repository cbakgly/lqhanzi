# -*- coding:utf8 -*-
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework import viewsets
from rest_framework import serializers

import django_filters

from ..pagination import NumberPagination
from ..models import CreditsRedeem
from ..auth import IsBusinessMember


class RedeemFilter(django_filters.FilterSet):
    """
    根据用户来获取
    """

    class Meta:
        model = CreditsRedeem
        fields = ["applied_by__username", "status"]


class RedeemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditsRedeem
        fields = "__all__"


class RedeemSerializerVersion1(serializers.ModelSerializer):
    class Meta:
        model = CreditsRedeem
        fields = "__all__"
        depth = 1


class RedeemViewSet(viewsets.ModelViewSet):
    """
    积分兑换
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsBusinessMember)

    queryset = CreditsRedeem.objects.all()
    filter_class = RedeemFilter
    pagination_class = NumberPagination
    serializer_class = RedeemSerializer

    @list_route()
    def certain_user_redeem(self, request, *args, **kwargs):
        user = request.user
        user_credits = user.applier.all()
        serializer = RedeemSerializer(user_credits, many=True)

        return Response(serializer.data)
