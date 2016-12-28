# -*- coding:utf8 -*-
import django_filters
import models


class DiaryFilter(django_filters.rest_framework.FilterSet):
    """
    根据用户id和时间来筛选
    """
    c_t = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = models.Diaries
        fields = ['user_id', 'c_t']
