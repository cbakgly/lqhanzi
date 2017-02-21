# -*- coding:utf8 -*-
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework import viewsets
from rest_framework import serializers

import django_filters

from ..pagination import NumberPagination
from ..models import CreditsRedeem, Reward
from ..auth import IsBusinessMember


class RedeemFilter(django_filters.FilterSet):

    """
    根据用户来获取
    """

    class Meta:
        model = CreditsRedeem
        fields = ["applied_by__username", "status"]


redeem_status_choices = {0: u'申请中', 1: u'已受理', 2: u'已完成'}


class RedeemSerializer(serializers.ModelSerializer):
    status_name = serializers.SerializerMethodField()

    class Meta:
        model = CreditsRedeem
        fields = "__all__"

    def get_status_name(self, obj):
        status = obj.status
        return redeem_status_choices[status]


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

    @list_route(methods=['POST'])
    def create_redeem(self, request, *args, **kwargs):
        reward_id = request.data['reward_id']
        reward = list(Reward.objects.filter(pk=reward_id))[0]
        data = {
            'applied_by': request.user,
            'reward_name': reward.reward_name,
            'cost_credits': request.data['need_credits'],
            'status': 0,
            'remark': request.data['remark']
        }
        new_redeem = CreditsRedeem(applied_by=data["applied_by"])
        for key in data.keys():
            setattr(new_redeem, key, data.get(key, getattr(new_redeem, key)))
        new_redeem.save()
        return Response('success')

    @list_route(methods=['POST'])
    def delete_redeem(self, request, *args, **kwargs):
        redeem_id = request.data['redeem_id']
        redeem_to_withdraw = CreditsRedeem.objects.get(pk=redeem_id)
        delete_status = redeem_to_withdraw.delete()
        return Response(delete_status)
