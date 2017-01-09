# -*- coding:utf8 -*-
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters

from ..pagination import NumberPagination
from ..models import KoreanDedup, InterDictDedup, HanziSet
from ..utils import get_korean_char_pic_variant_path, get_taiwan_char_pic_path
from ..filters import fields_or_filter_method
from ..enums import getenum_source


class KoreanDedupSerializer(serializers.ModelSerializer):
    class Meta:
        model = KoreanDedup
        fields = "__all__"
        depth = 0


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
        code = ret['hanzi_pic_id'][-1] if ret['hanzi_pic_id'] else False
        ret['hanzi_pic_path'] = get_korean_char_pic_variant_path(code) + ret['hanzi_pic_id'] + ('.png') if code else ''
        ret['source_display'] = instance.get_source_display()
        ret['is_draft_equals_review_display'] = instance.get_is_draft_equals_review_display()
        ret['is_review_equals_final_display'] = instance.get_is_review_equals_final_display()
        ret['is_checked_display'] = instance.get_is_checked_display()
        ret['is_submitted_display'] = instance.get_is_submitted_display()

        tw_hanzi = ret['inter_dict_dup_hanzi_draft']
        if tw_hanzi and len(tw_hanzi.decode('utf-8')) == 1:
            ret['is_draft_pic'] = 0
            row = HanziSet.objects.get(hanzi_char=tw_hanzi, source=getenum_source('tw'))
            ret['inter_dict_dup_hanzi_draft_seq_id'] = row.seq_id
        else:
            ret['is_draft_pic'] = 1
            ret['inter_dict_dup_hanzi_draft_path'] = get_taiwan_char_pic_path() + tw_hanzi[:2] + '/' + tw_hanzi + '.png' if tw_hanzi else ''

        tw_hanzi = ret['inter_dict_dup_hanzi_review']
        if tw_hanzi and len(tw_hanzi.decode('utf-8')) == 1:
            ret['is_review_pic'] = 0
            row = HanziSet.objects.get(hanzi_char=tw_hanzi, source=getenum_source('tw'))
            ret['inter_dict_dup_hanzi_review_seq_id'] = row.seq_id
        else:
            ret['is_review_pic'] = 1
            ret['inter_dict_dup_hanzi_review_path'] = get_taiwan_char_pic_path() + tw_hanzi[:2] + '/' + tw_hanzi + '.png' if tw_hanzi else ''

        tw_hanzi = ret['inter_dict_dup_hanzi_final']
        if tw_hanzi and len(tw_hanzi.decode('utf-8')) == 1:
            ret['is_final_pic'] = 0
            row = HanziSet.objects.get(hanzi_char=tw_hanzi, source=getenum_source('tw'))
            ret['inter_dict_dup_hanzi_final_seq_id'] = row.seq_id
        else:
            ret['is_final_pic'] = 1
            ret['inter_dict_dup_hanzi_final_path'] = get_taiwan_char_pic_path() + tw_hanzi[:2] + '/' + tw_hanzi + '.png' if tw_hanzi else ''

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
