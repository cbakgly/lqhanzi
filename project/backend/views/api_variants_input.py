# -*- coding:utf8 -*-
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters

from ..pagination import NumberPagination
from ..models import VariantsInput
from ..filters import NumberInFilter


class VariantsInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantsInput
        fields = "__all__"
        depth = 0


class VariantsInputFilter(django_filters.FilterSet):
    """
    异体字拆字过滤器
    """
    update_time_in = NumberInFilter(name='business_type', lookup_expr='in')

    class Meta:
        model = VariantsInput
        fields = ["page_num", "update_time_in", "hanzi_char_draft", "hanzi_pic_id_draft", "variant_type_draft",
                  "std_hanzi_draft", "notes_draft", "hanzi_char_review", "hanzi_pic_id_review", "variant_type_review",
                  "std_hanzi_review", "notes_review", "hanzi_char_final", "hanzi_pic_id_final", "variant_type_final",
                  "std_hanzi_final", "notes_final", "is_checked", "is_submitted", "is_draft_equals_review",
                  "is_review_equals_final"]


class VariantsInputViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = VariantsInput.objects.all()
    filter_class = VariantsInputFilter
    pagination_class = NumberPagination
    serializer_class = VariantsInputSerializer
