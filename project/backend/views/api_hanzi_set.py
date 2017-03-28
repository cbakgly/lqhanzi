# -*- coding:utf8 -*-
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters

from ..pagination import NumberPagination
from ..models import HanziSet
from ..utils import get_pic_url_by_source_pic_name
from ..filters import fields_or_filter_method


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
        ret['hanzi_type_display'] = instance.get_hanzi_type_display()
        ret['source_display'] = instance.get_source_display()
        return ret


class HanziSetDedupSerializer(serializers.ModelSerializer):
    hanzi_pic = serializers.SerializerMethodField()

    class Meta:
        model = HanziSet
        exclude = ["hanzi_type",
                   "variant_type",
                   "as_std_hanzi",
                   "pinyin",
                   "radical",
                   # "strokes",
                   "zheng_code",
                   "wubi",
                   "dup_count",
                   "inter_dict_dup_hanzi",
                   "korean_dup_hanzi",
                   "is_korean_redundant",
                   "is_inter_dict_redundant",
                   "structure",
                   "min_split",
                   "max_split",
                   "mix_split",
                   "deform_split",
                   "similar_parts",
                   "stroke_serial",
                   "remark",
                   "c_t",
                   "u_t",
                   "std_hanzi",
                   "source"
                   #"hanzi_pic_id",
                   # "hanzi_char"
                   ]

    def get_hanzi_pic(self, obj):
        #    if not obj.hanzi_char:
        return get_pic_url_by_source_pic_name(obj.source, obj.hanzi_pic_id)
    #    else:
    #        return obj.hanzi_char


class HanziSetFilter(django_filters.FilterSet):
    '''
    异体字拆字过滤器
    '''
    u_t = django_filters.DateTimeFromToRangeFilter()
    split = django_filters.CharFilter(name=["min_split", "max_split", "mix_split", "deform_split"], method=fields_or_filter_method)

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
