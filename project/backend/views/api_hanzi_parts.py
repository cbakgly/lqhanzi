# -*- coding:utf8 -*-
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import django_filters

from ..models import LqHanziPart


class HanziPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = LqHanziPart
        fields = ('input', 'display', 'strokes', 'stroke_hspnz')
        depth = 0


class HanziPartFilter(django_filters.FilterSet):
    """
    异体字拆字过滤器
    """

    class Meta:
        model = LqHanziPart
        fields = "__all__"


class HanziPartViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)

    queryset = LqHanziPart.objects.order_by('strokes', 'stroke_order')
    filter_class = HanziPartFilter
    pagination_class = None
    serializer_class = HanziPartSerializer
