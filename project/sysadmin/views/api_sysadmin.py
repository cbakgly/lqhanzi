from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import filters
from sysadmin.models import User
from sysadmin.models import Operation
from rest_framework.response import Response
from django.db.models import Q
from datetime import datetime
from rest_framework import serializers
import rest_framework_filters as filters

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ('message', 'logtype', 'logtime', 'user')

    def create(self, validated_data):
        user = validated_data['user']
        operation = Operation(user=user, logtype=validated_data['logtype'], \
        logtime=validated_data['logtime'], message=validated_data['message'])

        operation.save()
        return Operation(**validated_data)

class OperationFilter(filters.FilterSet):
    logtime = filters.DateFromToRangeFilter()
    class Meta:
        model = Operation
        fields = {
                'logtype': ['exact'],
                'user__username': ['exact'],
                'message': ['in', 'startswith'],
        }

class OperationViewSet(viewsets.ModelViewSet):
    serializer_class = OperationSerializer
    filter_class = OperationFilter
    queryset = Operation.objects.all()
