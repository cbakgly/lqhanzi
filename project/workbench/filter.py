# -*- coding:utf8 -*-
from rest_framework import filters
import django_filters
import models


class DiaryFilter(django_filters.rest_framework.FilterSet):
    """
    根据用户id和时间来筛选
    """
    c_t = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = models.Diary
        fields = ['user_id', 'c_t']
