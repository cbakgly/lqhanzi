import django_filters
from django.db.models import Q


class NumberInFilter(django_filters.filters.BaseInFilter, django_filters.filters.NumberFilter):
    pass


def fields_or_filter_method(qs, fields, value):
    """
    Return a queryset filtering by fields[0] = value or fields[1] = value or ...
    :param qs: queryset passed in
    :param fields: user-specified field list
    :param value: checking against
    :return: filtered queryset
    """
    exp = Q()
    exp.connector = 'OR'
    for field in fields:
        exp.add((field, value), 'OR')

    return qs.filter(exp)
