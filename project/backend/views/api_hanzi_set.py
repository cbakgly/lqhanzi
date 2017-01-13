# -*- coding:utf8 -*-
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters

from ..pagination import NumberPagination
from ..models import HanziSet
from ..utils import get_pic_url_by_source_pic_name


class HanziSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = HanziSet
        fields = "__all__"

    def to_representation(self, instance):
        ret = super(HanziSetSerializer, self).to_representation(instance)
        ret['hanzi_pic_path'] = get_pic_url_by_source_pic_name(ret['source'], ret['hanzi_pic_id'])
        ret['is_inter_dict_redundant_display'] = instance.get_is_inter_dict_redundant_display()
        ret['is_korean_redundant_display'] = instance.get_is_korean_redundant_display()
        ret['variant_type_display'] = instance.get_variant_type_display()
        ret['hanzi_type'] = instance.get_hanzi_type_display()
        return ret


class HanziSetFilter(django_filters.FilterSet):

    """
    异体字拆字过滤器
    """
    u_t_span = django_filters.DateTimeFromToRangeFilter(name="u_t")

    class Meta:
        model = HanziSet
        fields = "__all__"


class HanziSetViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = HanziSet.objects.all()
    filter_class = HanziSetFilter
    pagination_class = NumberPagination
    serializer_class = HanziSetSerializer
