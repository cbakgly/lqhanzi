# -*- coding:utf8 -*-
# import rest_framework_filters as filters
import django_filters as filters
import models


class DiaryFilter(filters.FilterSet):
    """
    根据用户id和时间来筛选
    """
    c_t = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = models.Diaries
        fields = ['user', 'c_t']


class CreditFilter(filters.FilterSet):
    """
    根据用户id和时间来筛选
    """
    c_t = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = models.Credits
        fields = ['sort', 'user']
