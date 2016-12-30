# coding: utf-8
from __future__ import unicode_literals
from sysadmin.models import User
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.decorators import detail_route
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_204_NO_CONTENT
import rest_framework_filters as filters
from rest_framework.response import Response


# User management
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
            if getattr(validated_data, key) is not None:
                setattr(instance, key, validated_data.get(key, getattr(instance, key)))
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)
        ret['gender_display'] = instance.get_gender_display()
        return ret


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {'username', 'first_name', 'last_name', 'email', 'is_active', 'gender', 'mb'}


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and confirm it.")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")

        return data


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = UserSerializer
    filter_class = UserFilter
    queryset = User.objects.all()

    @detail_route(methods=['post', 'get'])
    def set_password(self, request, *args, **kwargs):
        if request.method == 'GET':
            serializer_class = PasswordSerializer
            return Response({'key': 'test'})

        serializer = PasswordSerializer(data=request.data)
        user = self.get_object()
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'Password set'})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
