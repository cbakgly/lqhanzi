# -*- coding:utf8 -*-
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters

from ..pagination import NumberPagination
from ..models import KoreanDedup, InterDictDedup, HanziSet
from ..utils import get_pic_url_by_source_pic_name
from ..filters import fields_or_filter_method
from ..enums import getenum_source


class KoreanDedupSerializer(serializers.ModelSerializer):
    class Meta:
        model = KoreanDedup
        fields = "__all__"
        depth = 0

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

    class Meta:
        model = KoreanDedup
        fields = ("__all__")


class KoreanDedupViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = KoreanDedup.objects.all()
    filter_class = KoreanDedupFilter
    pagination_class = NumberPagination
    serializer_class = KoreanDedupSerializer


class InterDictDedupSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterDictDedup
        fields = "__all__"
        depth = 0

    def to_representation(self, instance):
        ret = super(InterDictDedupSerializer, self).to_representation(instance)
        ret['hanzi_pic_path'] = get_pic_url_by_source_pic_name(getenum_source('korean'), ret['hanzi_pic_id'])
        ret['source_display'] = instance.get_source_display()
        ret['is_draft_equals_review_display'] = instance.get_is_draft_equals_review_display()
        ret['is_review_equals_final_display'] = instance.get_is_review_equals_final_display()
        ret['is_checked_display'] = instance.get_is_checked_display()
        ret['is_submitted_display'] = instance.get_is_submitted_display()

        tw_hanzi = ret['inter_dict_dup_hanzi_draft']
        if tw_hanzi and len(tw_hanzi) <= 2:
            ret['is_draft_pic'] = 0
            row = HanziSet.objects.filter(hanzi_char=tw_hanzi, source=getenum_source('taiwan'))
            ret['inter_dict_dup_hanzi_draft_seq_id'] = row[0].seq_id if row else ''
        else:
            ret['is_draft_pic'] = 1
            ret['inter_dict_dup_hanzi_draft_path'] = get_pic_url_by_source_pic_name(getenum_source('taiwan'), tw_hanzi)

        tw_hanzi = ret['inter_dict_dup_hanzi_review']
        if tw_hanzi and len(tw_hanzi) <= 2:
            ret['is_review_pic'] = 0
            row = HanziSet.objects.filter(hanzi_char=tw_hanzi, source=getenum_source('taiwan'))
            ret['inter_dict_dup_hanzi_review_seq_id'] = row[0].seq_id if row else ''
        else:
            ret['is_review_pic'] = 1
            ret['inter_dict_dup_hanzi_review_path'] = get_pic_url_by_source_pic_name(getenum_source('taiwan'), tw_hanzi)

        tw_hanzi = ret['inter_dict_dup_hanzi_final']
        if tw_hanzi and len(tw_hanzi) <= 2:
            ret['is_final_pic'] = 0
            row = HanziSet.objects.filter(hanzi_char=tw_hanzi, source=getenum_source('taiwan'))
            ret['inter_dict_dup_hanzi_final_seq_id'] = row[0].seq_id if row else ''
        else:
            ret['is_final_pic'] = 1
            ret['inter_dict_dup_hanzi_final_path'] = get_pic_url_by_source_pic_name(getenum_source('taiwan'), tw_hanzi)

        return ret


class InterDictDedupFilter(django_filters.FilterSet):
    """
    异体字拆字过滤器
    """
    inter_dict_dup_hanzi = django_filters.CharFilter(name=["inter_dict_dup_hanzi_draft", "inter_dict_dup_hanzi_review", "inter_dict_dup_hanzi_final"], method=fields_or_filter_method)

    class Meta:
        model = InterDictDedup
        fields = ("hanzi_pic_id", "inter_dict_dup_hanzi", "std_hanzi", "is_draft_equals_review", "is_review_equals_final", "is_checked", "is_submitted")


class InterDictDedupViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = InterDictDedup.objects.exclude(inter_dict_dup_hanzi_final='', inter_dict_dup_hanzi_review='', inter_dict_dup_hanzi_draft='')
    filter_class = InterDictDedupFilter
    pagination_class = NumberPagination
    serializer_class = InterDictDedupSerializer
