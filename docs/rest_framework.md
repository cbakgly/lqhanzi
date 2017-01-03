
坑列表：

1 django-filters 要用 0.15版本
2 排序功能在filter类中加上如下一行，如按id排序
ordering = django_filters.OrderingFilter(fields=('id',))
3 文档提到的django-filters.rest_framework.FilterSet不要用，使用django_filters.FilterSet

