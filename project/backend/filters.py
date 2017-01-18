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


class NotEmptyFilter(django_filters.NumberFilter):
    def filter(self, qs, value):
        if value is not None:
            if value == 1:
                return qs.exclude(**{'%s__isnull' % self.name: True}).exclude(**{'%s__exact' % self.name: ""})
            elif value == 0:
                return qs.filter(Q(**{'%s__isnull' % self.name: True}) | Q(**{'%s__exact' % self.name: ""}))
        return qs
