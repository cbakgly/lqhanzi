# -*- coding:utf8 -*-

from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework import viewsets
from rest_framework import serializers

from django_filters.rest_framework import DjangoFilterBackend
import django_filters


from ..pagination import NumberPagination
from ..models import CreditsRedeem


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
        fields = ("__all__")


class RedeemSerializerVersion1(serializers.ModelSerializer):
    class Meta:
        model = CreditsRedeem
        fields = ("__all__")
        depth = 1


class RedeemViewSet(viewsets.ModelViewSet):
    """
    积分兑换
    """
    queryset = CreditsRedeem.objects.all()
    filter_class = RedeemFilter
    filter_backends = (DjangoFilterBackend,)
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