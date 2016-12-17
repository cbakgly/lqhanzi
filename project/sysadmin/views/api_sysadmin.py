# encoding: utf-8
from __future__ import unicode_literals
from sysadmin.models import User
from sysadmin.models import Operation
from rest_framework import viewsets
from rest_framework import serializers
import rest_framework_filters as filters

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'gender', 'mb', 'qq', 'address')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        for key in ('username', 'first_name', 'last_name', 'email', 'is_active', 'gender', 'mb', 'qq'):
            setattr(instance, key, validated_data.get(key, getattr(instance, key)))
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
        
class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {'username', 'first_name', 'last_name', 'email', 'is_active', 'gender', 'mb'}
        
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    filter_class = UserFilter
    queryset = User.objects.all()

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
    serializer_class = OperationSerializer
    filter_class = OperationFilter
    queryset = Operation.objects.all()
