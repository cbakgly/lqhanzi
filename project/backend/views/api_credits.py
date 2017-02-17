# -*- coding:utf8 -*-
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters

from ..models import Credits, CreditsRedeem
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

        user_credits = list(Credits.objects.filter(user_id=user.id).exclude(credit=0))
        total, split, input, dedup, other = 0, 0, 0, 0, 0
        for user_credit in user_credits:
            if user_credit.sort == 0:
                total = float(user_credit.credit)
            elif user_credit.sort == 1:
                split = user_credit.credit
            elif user_credit.sort == 2:
                input = user_credit.credit
            elif user_credit.sort == 5:
                dedup = user_credit.credit
        other = total - split -input - dedup
        split = split/total*100
        input = input/total*100
        dedup = dedup/total*100
        other = other/total*100
        credit_des = "拆字：%.0f%%，录入：%.0f%%，去重:%.0f%%，其他：%.0f%%" % (split,input,dedup,other)
        credit_redeem = CreditsRedeem.objects.filter(applied_by=user).values("cost_credits").aggregate(Sum("cost_credits"))
        r = Response({'sum_credit':total,'credit_detail':credit_des,'credit_redeem':credit_redeem['cost_credits__sum']})
        return r

    @list_route()
    def searchcredit(self, request, *args, **kwargs):
        sort = request.query_params['select_sort']
        name = request.query_params['search_name']
        if sort is -1:
            search_result = Credits.objects.filter(user__username__contains=name)
        else:
            search_result = Credits.objects.filter(user__username__contains=name, sort=sort)
        return Response(self.serializer_class(search_result,many=True).data)
