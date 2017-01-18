# -*- coding:utf8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status

from ..pagination import NumberPagination
from ..models import VariantsInput
from ..filters import NumberInFilter
from ..enums import getenum_task_business_status, getenum_business_stage
from task_func import assign_input_task


def update_tasks_status(variants_input):
    tasks = list(variants_input.task.all())
    task_dict = {}
    for t in tasks:
        task_dict[t.business_stage] = t
    draft = task_dict[getenum_business_stage('init')]
    review = task_dict[getenum_business_stage('review')]
    final = task_dict[getenum_business_stage('final')]
    origin_task = draft
    if draft.task_status == getenum_task_business_status("ongoing"):
        draft.task_status = getenum_task_business_status("completed")
        draft.completed_at = timezone.now()
        review.task_status = getenum_task_business_status("to_be_arranged")
        variants_input.save()
        draft.save()
        review.save()
    elif review.task_status == getenum_task_business_status("ongoing"):
        review.task_status = getenum_task_business_status("completed")
        review.completed_at = timezone.now()
        final.task_status = getenum_task_business_status("to_be_arranged")
        variants_input.is_draft_equals_review = variants_input.inter_dict_dup_hanzi_draft is variants_input.inter_dict_dup_hanzi_review
        variants_input.save()
        review.save()
        final.save()
        origin_task = review
    elif final.task_status == getenum_task_business_status("ongoing"):
        final.task_status = getenum_task_business_status("completed")
        final.completed_at = timezone.now()
        variants_input.is_review_equals_final = variants_input.inter_dict_dup_hanzi_review is variants_input.inter_dict_dup_hanzi_final
        variants_input.save()
        final.save()
        origin_task = final
    else:
        pass
    return origin_task


class VariantsInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantsInput
        fields = "__all__"
        depth = 0

    def to_representation(self, instance):
        ret = super(VariantsInputSerializer, self).to_representation(instance)
        ret['variant_type_draft'] = instance.get_variant_type_draft_display()
        ret['is_del_draft'] = instance.get_is_del_draft_display()
        ret['variant_type_review'] = instance.get_variant_type_review_display()
        ret['is_del_review'] = instance.get_is_del_review_display()
        ret['variant_type_final'] = instance.get_variant_type_final_display()
        ret['is_del_final'] = instance.get_is_del_final_display()
        ret['is_draft_equals_review_display'] = instance.get_is_draft_equals_review_display()
        ret['is_review_equals_final_display'] = instance.get_is_review_equals_final_display()
        ret['is_checked_display'] = instance.get_is_checked_display()
        ret['is_submitted_display'] = instance.get_is_submitted_display()
        return ret


class VariantsInputSelectSerializer(serializers.ModelSerializer):

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
        fields = "__all__"


class VariantsInputViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = VariantsInput.objects.all()
    filter_class = VariantsInputFilter
    pagination_class = NumberPagination
    serializer_class = VariantsInputSerializer

    # 提交
    @detail_route(methods=["PUT", "GET", "PATCH"])
    def submit(self, request, *args, **kwargs):
        variants_input = self.get_object()
        serializer = VariantsInputSerializer(data=request.data)

        if serializer.is_valid():
            origin_task = update_tasks_status(variants_input)
            task_ele = origin_task.content_object
            for key in serializer.initial_data.keys():
                setattr(task_ele, key, serializer.initial_data.get(key, getattr(task_ele, key)))
            task_ele.save()
            serializer = self.serializer_class(task_ele)
            return Response(serializer.data)
        else:
            return Response(_("Inputdata Error!"))

            # 提交并转下一条

    @detail_route(methods=["PUT", "GET", "PATCH"])
    def submit_and_next(self, request, *args, **kwargs):
        variants_input = self.get_object()
        serializer = VariantsInputSerializer(data=request.data)

        if serializer.is_valid():
            origin_task = update_tasks_status(variants_input)
            task_ele = origin_task.content_object
            for key in serializer.initial_data.keys():
                setattr(task_ele, key, serializer.initial_data.get(key, getattr(task_ele, key)))
            task_ele.save()

            task_package = origin_task.task_package
            task_plan = task_package.size
            task_num = len(list(task_package.tasks.all()))
            if task_num < task_plan:
                business_type = origin_task.business_type
                business_stage = origin_task.business_stage
                user = origin_task.user
                new_task = assign_input_task(business_type, business_stage, task_package, user)
                if new_task:
                    serializer = self.serializer_class(new_task.content_object)
                    return Response(serializer.data)
                else:
                    return Response(_("No more task today, have a try tommorrow!"), status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(_("This package is completed, please apply for a new one!"), status=status.HTTP_100_CONTINUE)
        return Response(_("Inputdata Error!"))
