# -*- coding:utf8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route
from rest_framework import status
from rest_framework.response import Response
import django_filters

from ..pagination import NumberPagination
from ..models import KoreanDupCharacters, HanziSet
from ..enums import getenum_source, getenum_business_stage, getenum_task_business_status
from api_hanzi_set import HanziSetDedupSerializer
from task_func import assign_task


class KoreanDupCharactersSerializer(serializers.ModelSerializer):
    korean_hanzi_sets = serializers.SerializerMethodField()
    tw_hanzi_sets = serializers.SerializerMethodField()

    class Meta:
        model = KoreanDupCharacters
        exclude = ["c_t", "u_t", "remark", "relation"]
        depth = 0

    def get_korean_hanzi_sets(self, obj):
        hanzi_set_qs = HanziSet.objects.filter(std_hanzi=obj.korean_variant).filter(source=getenum_source('korean'))
        return HanziSetDedupSerializer(hanzi_set_qs, many=True).data

    def get_tw_hanzi_sets(self, obj):
        hanzi_set_qs = HanziSet.objects.filter(std_hanzi=obj.korean_variant).filter(source=getenum_source('taiwan'))
        return HanziSetDedupSerializer(hanzi_set_qs, many=True).data


class KoreanDupCharSerializer(serializers.ModelSerializer):

    class Meta:
        model = KoreanDupCharacters
        exclude = ["c_t", "u_t", "remark", "relation"]
        depth = 0


class KoreanDupCharactersFilter(django_filters.FilterSet):
    """
    异体字拆字过滤器
    """

    class Meta:
        model = KoreanDupCharacters
        fields = ("__all__")


def update_tasks_status(variants_dedup):
    tasks = list(variants_dedup.task.all())
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
        draft.save()
        review.save()
    elif review.task_status == getenum_task_business_status("ongoing"):
        review.task_status = getenum_task_business_status("completed")
        review.completed_at = timezone.now()
        final.task_status = getenum_task_business_status("to_be_arranged")
        review.save()
        final.save()
        origin_task = review
    elif final.task_status == getenum_task_business_status("ongoing"):
        final.task_status = getenum_task_business_status("completed")
        final.completed_at = timezone.now()
        final.save()
        origin_task = final
    else:
        pass
    return origin_task


class KoreanTaiwanDupCharactersViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = KoreanDupCharacters.objects.all()
    filter_class = KoreanDupCharactersFilter
    pagination_class = NumberPagination
    serializer_class = KoreanDupCharactersSerializer

    # 提交
    @detail_route(methods=["PUT", "GET", "PATCH"])
    def submit(self, request, *args, **kwargs):
        variants_input = self.get_object()
        origin_task = update_tasks_status(variants_input)
        if origin_task:
            return Response(_("Succeess！"), status=status.HTTP_200_OK)
        else:
            return Response(_("Failed!"), status=status.HTTP_400_BAD_REQUEST)


    # 提交并转下一条
    @detail_route(methods=["PUT", "GET", "PATCH"])
    def submit_and_next(self, request, *args, **kwargs):
        variants_input = self.get_object()
        origin_task = update_tasks_status(variants_input)
        if origin_task:
            task_package = origin_task.task_package
            task_plan = task_package.size
            business_type = origin_task.business_type
            task_num = len(list(task_package.tasks.filter(business_type=business_type)))
            if task_num < task_plan:

                business_stage = origin_task.business_stage
                user = origin_task.user
                new_task = assign_task(business_type, business_stage, task_package, user)
                if type(new_task) is not Response:
                    serializer = self.serializer_class(new_task.content_object)
                    return Response(serializer.data)
                else:
                    return Response(_("No more task today, have a try tommorrow!"), status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(_("This package is completed, please apply for a new one!"), status=status.HTTP_100_CONTINUE)
        return Response(_("Inputdata Error!"), status=status.HTTP_400_BAD_REQUEST)
