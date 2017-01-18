# -*- coding:utf8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import connection
from django.db.models.query import RawQuerySet
from django.utils.functional import cached_property
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route
from rest_framework.response import Response
import django_filters

from ..pagination import NumberPagination
from ..models import KoreanDedup, InterDictDedup, HanziSet
from ..utils import get_pic_url_by_source_pic_name
from ..filters import fields_or_filter_method
from ..enums import getenum_source, getenum_task_business_status, getenum_business_stage
from task_func import create_task


class KoreanDedupSerializer(serializers.ModelSerializer):
    class Meta:
        model = KoreanDedup
        fields = "__all__"

    def to_representation(self, instance):
        ret = super(KoreanDedupSerializer, self).to_representation(instance)
        ret['hanzi_pic_path'] = get_pic_url_by_source_pic_name(getenum_source('korean'), ret['hanzi_pic_id'])
        ret['variant_type_display'] = instance.get_variant_type_display()
        ret['hanzi_type'] = instance.get_hanzi_type_display()
        return ret


class KoreanDedupFilter(django_filters.FilterSet):
    """
    异体字拆字过滤器
    """

    class Meta:
        model = KoreanDedup
        fields = "__all__"


class KoreanDedupViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    sql = """
    select r.* from `lq_korean_dup_zheng_codes` h
    left join lq_korean_dedup r on h.zheng_code = r.zheng_code
    where h.page_num = %d
    order by h.id
    """
    queryset = KoreanDedup.objects.all()
    filter_class = KoreanDedupFilter
    pagination_class = NumberPagination
    serializer_class = KoreanDedupSerializer
    pagination_class.page_size = 100

    @cached_property
    def total_page(self):
        cursor = connection.cursor()
        cursor.execute("select max(page_num) from lq_korean_dup_zheng_codes;")
        row = cursor.fetchone()
        return row[0]

    def list(self, request, *args, **kwargs):
        page_number = int(request.query_params.get(self.paginator.page_query_param, 1))
        page_size = self.paginator.get_page_size(request)

        # Raw query set doesn't have count() and getitem() used in pagination
        # We provide one in order to make paging run smoothly
        # Arbitrarily set them so it makes paging as what we intend to, here, 100/p, 100*total_page
        queryset = KoreanDedup.objects.raw(self.sql % (page_number))
        queryset.count = lambda: self.total_page * page_size
        RawQuerySet.__getitem__ = lambda this, k: list(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class InterDictDedupSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterDictDedup
        fields = "__all__"

    def to_representation(self, instance):
        ret = super(InterDictDedupSerializer, self).to_representation(instance)
        ret['hanzi_pic_path'] = get_pic_url_by_source_pic_name(getenum_source('korean'), ret['hanzi_pic_id'])
        ret['source_display'] = instance.get_source_display()
        ret['is_draft_equals_review_display'] = instance.get_is_draft_equals_review_display()
        ret['is_review_equals_final_display'] = instance.get_is_review_equals_final_display()
        ret['is_checked_display'] = instance.get_is_checked_display()
        ret['is_submitted_display'] = instance.get_is_submitted_display()

        tw_hanzi = ret['inter_dict_dup_hanzi_draft']
        if tw_hanzi and len(tw_hanzi) <= 2:
            ret['is_draft_pic'] = 0
            row = HanziSet.objects.filter(hanzi_char=tw_hanzi, source=getenum_source('taiwan'))
            ret['inter_dict_dup_hanzi_draft_seq_id'] = row[0].seq_id if row else ''
        else:
            ret['is_draft_pic'] = 1
            ret['inter_dict_dup_hanzi_draft_path'] = get_pic_url_by_source_pic_name(getenum_source('taiwan'), tw_hanzi)

        tw_hanzi = ret['inter_dict_dup_hanzi_review']
        if tw_hanzi and len(tw_hanzi) <= 2:
            ret['is_review_pic'] = 0
            row = HanziSet.objects.filter(hanzi_char=tw_hanzi, source=getenum_source('taiwan'))
            ret['inter_dict_dup_hanzi_review_seq_id'] = row[0].seq_id if row else ''
        else:
            ret['is_review_pic'] = 1
            ret['inter_dict_dup_hanzi_review_path'] = get_pic_url_by_source_pic_name(getenum_source('taiwan'), tw_hanzi)

        tw_hanzi = ret['inter_dict_dup_hanzi_final']
        if tw_hanzi and len(tw_hanzi) <= 2:
            ret['is_final_pic'] = 0
            row = HanziSet.objects.filter(hanzi_char=tw_hanzi, source=getenum_source('taiwan'))
            ret['inter_dict_dup_hanzi_final_seq_id'] = row[0].seq_id if row else ''
        else:
            ret['is_final_pic'] = 1
            ret['inter_dict_dup_hanzi_final_path'] = get_pic_url_by_source_pic_name(getenum_source('taiwan'), tw_hanzi)

        return ret


class InterDictDedupFilter(django_filters.FilterSet):
    """
    异体字拆字过滤器
    """
    inter_dict_dup_hanzi = django_filters.CharFilter(name=["inter_dict_dup_hanzi_draft", "inter_dict_dup_hanzi_review", "inter_dict_dup_hanzi_final"], method=fields_or_filter_method)
    u_t_span = django_filters.DateTimeFromToRangeFilter(name="u_t")

    class Meta:
        model = InterDictDedup
        fields = "__all__"


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
        variants_dedup.save()
        draft.save()
        review.save()
    elif review.task_status == getenum_task_business_status("ongoing"):
        review.task_status = getenum_task_business_status("completed")
        review.completed_at = timezone.now()
        final.task_status = getenum_task_business_status("to_be_arranged")
        variants_dedup.is_draft_equals_review = variants_dedup.inter_dict_dup_hanzi_draft is variants_dedup.inter_dict_dup_hanzi_review
        variants_dedup.save()
        review.save()
        final.save()
        origin_task = review
    elif final.task_status == getenum_task_business_status("ongoing"):
        final.task_status = getenum_task_business_status("completed")
        final.completed_at = timezone.now()
        variants_dedup.is_review_equals_final = variants_dedup.inter_dict_dup_hanzi_review is variants_dedup.inter_dict_dup_hanzi_final
        variants_dedup.save()
        final.save()
        origin_task = final
    else:
        pass
    return origin_task


class InterDictDedupViewSet(viewsets.ModelViewSet):
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)

    queryset = InterDictDedup.objects.exclude(inter_dict_dup_hanzi_final='', inter_dict_dup_hanzi_review='', inter_dict_dup_hanzi_draft='')
    filter_class = InterDictDedupFilter
    pagination_class = NumberPagination
    serializer_class = InterDictDedupSerializer

    # 提交 此处提交为单个字提交,非页面提交
    @detail_route(methods=["PUT", "GET", "PATCH"])
    def submit_single_variant(self, request, *args, **kwargs):
        variants_dedup = self.get_object()
        serializer = InterDictDedupSerializer(data=request.data)

        if serializer.is_valid():
            new_task_data = {
                'user': request.user,
                'task_package': request.query_params['task_package'],
                'content': variants_dedup
            }
            business_stage = create_task(new_task_data)
            if business_stage is 1:
                variants_dedup.inter_dict_dup_hanzi_draft = serializer.initial_data['inter_dict_dup_hanzi_draft']
            elif business_stage is 2:
                variants_dedup.inter_dict_dup_hanzi_review = serializer.initial_data['inter_dict_dup_hanzi_review']
            else:
                variants_dedup.inter_dict_dup_hanzi_final = serializer.initial_data['inter_dict_dup_hanzi_final']
            variants_dedup.save()
            serializer = self.serializer_class(variants_dedup)
            return Response(serializer.data)
        else:
            return Response(_("Inputdata Error!"))
