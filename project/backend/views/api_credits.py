# -*- coding:utf8 -*-
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters

from ..models import Credits, Tasks
from ..pagination import LimitOffsetPagination
from ..auth import IsBusinessMember


class CreditSerializer(serializers.ModelSerializer):
    rank = serializers.SerializerMethodField()
    sort_name = serializers.SerializerMethodField()

    class Meta:
        model = Credits
        fields = "__all__"
        depth = 1

    def get_rank(self, obj):
        ranks = {}
        credit_set = Credits.objects.all()
        if obj:
            for i in range(0, 10):
                ranks[i] = []

            for c in credit_set:
                cd = c.credit
                cs = c.sort
                if cd not in ranks[cs]:
                    ranks[cs].append(cd)
            for i in range(0, 10):
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
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsBusinessMember)

    queryset = Credits.objects.all()
    serializer_class = CreditSerializer
    filter_class = CreditFilter
    pagination_class = LimitOffsetPagination

    @list_route()
    def certain_user_credits(self, request, *args, **kwargs):
        user = request.user
        user_credits = user.user_credits.exclude(credit=0)
        serializer = self.serializer_class(user_credits, many=True)
        return Response(serializer.data)

    @list_route()
    def calculate_user_credits(self, request, *args, **kwargs):
        user = request.user
        #sum_credits = Tasks.objects.filter(user_id=user.id).values("credits").aggregate(Sum("credits"))
        user_credit = self.serializer_class(Credits.objects.filter(user_id=user.id).exclude(credit=0),many=True)
        r = Response(user_credit.data)
        print r['1']
        return Response(user_credit.data)

    @list_route()
    def searchcredit(self, request, *args, **kwargs):
        sort = request.query_params['select_sort']
        name = request.query_params['search_name']
        if sort is -1:
            search_result = Credits.objects.filter(user__username__contains=name)
        else:
            search_result = Credits.objects.filter(user__username__contains=name, sort=sort)
        return Response(self.serializer_class(search_result,many=True).data)
