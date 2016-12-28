# encoding: utf-8
from __future__ import unicode_literals
from sysadmin.models import Operation
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import rest_framework_filters as filters


# Operation log management
class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ('id', 'message', 'logtype', 'logtime', 'user')

    def create(self, validated_data):
        user = validated_data['user']
        operation = Operation(user=user, logtype=validated_data['logtype'], message=validated_data['message'])
        operation.save()
        return Operation(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.logtype = validated_data.get('logtype', instance.logtype)
        instance.message = validated_data.get('message', instance.message)
        instance.save()
        return instance


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
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = OperationSerializer
    filter_class = OperationFilter
    queryset = Operation.objects.all()
