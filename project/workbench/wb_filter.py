# -*- coding:utf8 -*-
# import rest_framework_filters as filters
import django_filters as filters
import models


class DiaryFilter(filters.FilterSet):
    """
    根据用户id和时间来筛选
    """
    c_t = filters.DateFromToRangeFilter()

    class Meta:
        model = models.Diaries
        fields = ["user__username", "c_t"]


class CreditFilter(filters.FilterSet):
    """
    根据用户id和时间来筛选
    """

    class Meta:
        model = models.Credits
        fields = ["id", "user", "sort", "user__username"]


class RedeemFilter(filters.FilterSet):
    """
    根据用户来获取
    """

    class Meta:
        model = models.CreditsRedeem
        fields = ["applied_by__username", "status"]


class VariantsSplitFilter(filters.FilterSet):
    """
    异体字拆字过滤器
    """

    class Meta:
        model = models.VariantsSplit
        fields = ("__all__")
