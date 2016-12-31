# encoding: utf-8
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

import rest_framework_filters as filters
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

    def to_representation(self, instance):
        ret = super(DiariesSerializer, self).to_representation(instance)
        ret['tag_choices_display'] = instance.get_tag_choices_display()
        return ret


class DiariesFilter(filters.FilterSet):
    c_t = filters.DateFromToRangeFilter()
    u_t = filters.DateFromToRangeFilter()

    class Meta:
        model = Diaries
        fields = '__all__'


class DiariesViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = DiariesSerializer
    filter_class = DiariesFilter
    queryset = Diaries.objects.all()
