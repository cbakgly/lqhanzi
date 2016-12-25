# encoding: utf-8
from __future__ import unicode_literals
from sysadmin.models import User
from sysadmin.models import Operation
from rest_framework import viewsets
from rest_framework import serializers
import rest_framework_filters as filters
from rest_framework.response import Response
from workbench.models import Diaries

# Operation log management
class DiariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diaries
        fields = '__all__'

    def create(self, validated_data):
        diary = Diaries.objects.create(**validated_data)
        return diary

    def update(self, instance, validated_data):
        return instance


class DiariesFilter(filters.FilterSet):
    c_t = filters.DateFromToRangeFilter()
    u_t = filters.DateFromToRangeFilter()

    class Meta:
        model = Diaries
        fields = '__all__'

class DiariesViewSet(viewsets.ModelViewSet):
    serializer_class = DiariesSerializer
    filter_class = DiariesFilter
    queryset = Diaries.objects.all()
