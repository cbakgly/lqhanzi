import django_filters


class NumberInFilter(django_filters.filters.BaseInFilter, django_filters.filters.NumberFilter):
    pass
