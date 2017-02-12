# -*- coding:utf8 -*-
import django_filters
from django.db import connection
from django.db.models.query import RawQuerySet
from django.utils.functional import cached_property
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from ..pagination import NumberPagination100
from ..models import KoreanDedup
from ..utils import get_pic_url_by_source_pic_name, is_search_request
from ..filters import NotEmptyFilter
from ..enums import getenum_source
from ..auth import IsBusinessMember

class KoreanDedupSerializer(serializers.ModelSerializer):
    class Meta:
        model = KoreanDedup
        fields = "__all__"

    def to_representation(self, instance):
        ret = super(KoreanDedupSerializer, self).to_representation(instance)
        ret['hanzi_pic_path'] = get_pic_url_by_source_pic_name(getenum_source('korean'), ret['hanzi_pic_id'])
        ret['variant_type_display'] = instance.get_variant_type_display()
        ret['hanzi_type'] = instance.get_hanzi_type_display()
        return ret


class KoreanDedupFilter(django_filters.FilterSet):
    """
    异体字拆字过滤器
    """
    has_dup = NotEmptyFilter(name='korean_dup_hanzi')

    class Meta:
        model = KoreanDedup
        fields = ['zheng_code', 'std_hanzi', 'hanzi_pic_id', 'has_dup']


class KoreanDedupViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsBusinessMember)

    sql = """
    select r.* from `lq_korean_dup_zheng_codes` h
    left join lq_korean_dedup r on h.zheng_code = r.zheng_code
    where h.page_num = %d
    """
    queryset = KoreanDedup.objects.all()
    filter_class = KoreanDedupFilter
    pagination_class = NumberPagination100
    serializer_class = KoreanDedupSerializer

    @cached_property
    def total_page(self):
        cursor = connection.cursor()
        cursor.execute("select max(page_num) from lq_korean_dup_zheng_codes;")
        row = cursor.fetchone()
        return row[0]

    def list(self, request, *args, **kwargs):
        if is_search_request(request.query_params, *KoreanDedupFilter.Meta.fields):
            qs = self.filter_queryset(self.get_queryset())
            self.pagination_class.page_size = api_settings.PAGE_SIZE
        else:
            page_number = int(request.query_params.get(self.paginator.page_query_param, 1))
            # if page_size_query_param is set, get its value
            page_size = self.paginator.get_page_size(request)

            # Rawqueryset doesn't have count() and getitem() to use in pagination
            # We provide them in order to utilize existing functions.
            qs = KoreanDedup.objects.raw(self.sql % (page_number))

            # Arbitrarily set them so it makes paging run as-is
            # It's paged as what we intend to, here, 100/p, 100*total_page
            qs.count = lambda: self.total_page * page_size
            RawQuerySet.__getitem__ = lambda this, k: list(qs)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
