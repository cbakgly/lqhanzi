# encoding: utf-8
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters
from django.db.models import Q

from ..models import Tasks, VariantsSplit, VariantsInput, KoreanDedup, InterDictDedup
from ..enums import getenum_business_type
from ..views import api_variants_split, api_variants_input, api_variants_dedup


# Task Packages management
class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'

    def create(self, validated_data):
        task = Tasks.objects.create(**validated_data)
        task.save()
        return task

    def update(self, instance, validated_data):
        for key in ['business_id', 'business_type', 'user', 'business_stage', 'task_status', 'credits', 'remark', 'completed_at', 'task_package']:
            if validated_data.get(key) is not None:  # Only Set values which is put.
                setattr(instance, key, validated_data.get(key, getattr(instance, key)))

            instance.save()

        return instance

    def to_representation(self, instance):
        ret = super(TasksSerializer, self).to_representation(instance)
        ret['business_type_display'] = instance.get_business_type_display()
        ret['business_stage_display'] = instance.get_business_stage_display()
        ret['task_status_display'] = instance.get_task_status_display()
        return ret


class TasksFilter(django_filters.FilterSet):
    assigned_at = django_filters.DateFromToRangeFilter()
    completed_at = django_filters.DateFromToRangeFilter()
    ordering = django_filters.OrderingFilter(fields=('id',))

    class Meta:
        model = Tasks
        fields = ('__all__')


class TasksViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = TasksSerializer
    filter_class = TasksFilter
    queryset = Tasks.objects.all()

    @list_route()
    def split(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser == 1:
            queryset = Tasks.objects.filter(business_type=getenum_business_type('split'))
            # queryset = Tasks.objects.filter(task_package=request.query_params['task_package'])
        else:
            queryset = Tasks.objects.filter(user_id=user.id).filter(business_type=getenum_business_type('split'))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @list_route()
    def input(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser == 1:
            queryset = Tasks.objects.filter(business_type=getenum_business_type('input'))
        else:
            queryset = Tasks.objects.filter(user_id=user.id).filter(business_type=getenum_business_type('input'))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @list_route()
    def dedup(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser == 1:
            queryset = Tasks.objects.filter(business_type=getenum_business_type('dedup'))
        else:
            queryset = Tasks.objects.filter(user_id=user.id).filter(business_type=getenum_business_type('dedup'))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ChoiceTasksViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Tasks.objects.all()
    serializer_class = None
    filter_class = None

    def api_choice(self, sql_code):
        pass

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        q1 = Q()
        q1.connector = "OR"
        if user.is_superuser == 1:
            tasks = Tasks.objects.filter(task_package=self.request.query_params['task_package'])
            for t in tasks:
                q1.children.append(('id', t.variant_split.id))
            queryset = self.api_choice(q1)
            # queryset = tasks.prefetch_related('variant_split')
        else:
            tasks = Tasks.objects.filter(user_id=user.id).filter(task_package=self.request.query_params['task_package'])
            for t in tasks:
                q1.children.append(('id', t.variant_split.id))
            queryset = self.api_choice(q1)
        return queryset


class SplitTasksViewSet(ChoiceTasksViewSet):
    serializer_class = api_variants_split.VariantsSplitSerializer
    filter_class = api_variants_split.VariantsSplitFilter

    def api_choice(self, sql_code):
        queryset = VariantsSplit.objects.filter(sql_code)
        return queryset


class InputTasksViewSet(ChoiceTasksViewSet):
    serializer_class = api_variants_input.VariantsInputSerializer
    filter_class = api_variants_input.VariantsInputFilter

    def api_choice(self, sql_code):
        queryset = VariantsInput.objects.filter(sql_code)
        return queryset


class KoreanDedupTasksViewSet(ChoiceTasksViewSet):
    serializer_class = api_variants_dedup.KoreanDedupSerializer
    filter_class = api_variants_dedup.KoreanDedupFilter

    def api_choice(self, sql_code):
        queryset = KoreanDedup.objects.filter(sql_code)
        return queryset


class InterDictDedupTasksViewSet(ChoiceTasksViewSet):
    serializer_class = api_variants_dedup.InterDictDedupSerializer
    filter_class = api_variants_dedup.InterDictDedupFilter

    def api_choice(self, sql_code):
        queryset = InterDictDedup.objects.filter(sql_code)
        return queryset
