# -*- coding:utf8 -*-
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters

from ..pagination import NumberPagination
from ..models import KoreanDupCharacters


class KoreanDupCharactersSerializer(serializers.ModelSerializer):
    class Meta:
        model = KoreanDupCharacters
        fields = "__all__"
        depth = 0


class KoreanDupCharactersFilter(django_filters.FilterSet):
    """
    异体字拆字过滤器
    """

    class Meta:
        model = KoreanDupCharacters
        fields = ("__all__")


class KoreanTaiwanDupCharactersViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = KoreanDupCharacters.objects.all()
    filter_class = KoreanDupCharactersFilter
    pagination_class = NumberPagination
    serializer_class = KoreanDupCharactersSerializer
