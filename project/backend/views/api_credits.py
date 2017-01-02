# -*- coding:utf8 -*-

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework import serializers
import django_filters.rest_framework

from ..models import Credits
from ..pagination import LimitOffsetPagination


class CreditSerializer(serializers.ModelSerializer):
    rank = serializers.SerializerMethodField()
    sort_name = serializers.SerializerMethodField()

    class Meta:
        model = Credits
        fields = "__all__"
        depth = 0

    def get_rank(self, obj):
        ranks = {}
        credit_set = Credits.objects.all()
        for i in range(1, 6):
            ranks[i] = []

        for c in credit_set:
            cd = c.credit
            cs = c.sort
            if cd not in ranks[cs]:
                ranks[cs].append(cd)
        for i in range(1, 6):
            ranks[i].sort()
            ranks[i].reverse()
        return ranks[obj.sort].index(obj.credit) + 1

    def get_sort_name(self, obj):
        for sc in Credits.sort_choices:
            if obj.sort == sc[0]:
                return sc[1]


class CreditFilter(django_filters.FilterSet):
    """
    根据用户id和时间来筛选
    """

    class Meta:
        model = Credits
        fields = ["id", "user", "sort", "credit", "user__username"]


class CreditViewSet(viewsets.ModelViewSet):
    """
    积分
    """
    queryset = Credits.objects.all()
    serializer_class = CreditSerializer
    filter_class = CreditFilter
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination

    @list_route()
    def certain_user_credits(self, request, *args, **kwargs):
        user = request.user
        user_credits = user.user_credits.all()
        serializer = CreditSerializer(user_credits, many=True)

        return Response(serializer.data)
