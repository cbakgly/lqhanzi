# encoding: utf-8
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters
from django.http import HttpResponseNotFound
from django.core.exceptions import MultipleObjectsReturned
from django.db.models.query import RawQuerySet

from ..pagination import NumberPagination
from ..models import Tasks, VariantsSplit, KoreanDedup, VariantsInput, KoreanDupCharacters, InputPage
from ..enums import getenum_business_type, getenum_task_status, getenum_business_stage
import api_variants_input
import api_variants_dedup
import api_variants_split
import api_korean_dup_characters
from task_func import assign_task


def reset_task(task):
    task.task_package = None
    task.assigned_at = None
    task.user = None
    task.task_status = 0
    task.save()

    return task


# Task Packages management
class TasksSerializer(serializers.ModelSerializer):
    task_ele = serializers.SerializerMethodField()

    class Meta:
        model = Tasks
        fields = "__all__"

    def create(self, validated_data):
        task = Tasks.objects.create(**validated_data)
        task.save()
        return task

    def update(self, instance, validated_data):
        for key in ['business_id', 'business_type', 'user', 'business_stage', 'task_status',
                    'credits', 'remark', 'completed_at', 'task_package']:
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

    def get_task_ele(self, obj):
        task_ele = obj.content_object
        if isinstance(task_ele, VariantsInput):
            ele_serializer = api_variants_input.VariantsInputSerializer
        elif isinstance(task_ele, VariantsSplit):
            ele_serializer = api_variants_split.VariantsSplitSerializer
        elif isinstance(task_ele, KoreanDedup):
            ele_serializer = api_variants_dedup.KoreanDedupSerializer
        elif isinstance(task_ele, KoreanDupCharacters):
            ele_serializer = api_korean_dup_characters.KoreanDupCharactersSerializer
        elif isinstance(task_ele, InputPage):
            ele_serializer = api_variants_input.InputPageSerializer
        else:
            ele_serializer = api_variants_dedup.InterDictDedupSerializer

        serialized_data = ele_serializer(task_ele).data
        return serialized_data


class TasksFilter(django_filters.FilterSet):
    assigned_at = django_filters.DateFromToRangeFilter()
    completed_at = django_filters.DateFromToRangeFilter()
    ordering = django_filters.OrderingFilter(fields=('id',))

    class Meta:
        model = Tasks
        fields = "__all__"


class TasksViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    pagination_class = NumberPagination
    serializer_class = TasksSerializer
    filter_class = TasksFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            qs = Tasks.objects.all()
        else:
            qs = Tasks.objects.filter(user_id=user.id)
        return qs

    # 拆字
    @list_route()
    def ongoing_split(self, request, *args, **kwargs):
        user = self.request.user
        source = self.request.query_params["source"]
        hanzi_char = self.request.query_params["hanzi_char"]
        similar_parts = self.request.query_params["similar_parts"]
        task_package = request.query_params["task_package"]
        business_type = getenum_business_type("split")
        if user.is_superuser == 1:
            tasks = Tasks.objects.filter(business_type=business_type).filter(task_status=getenum_task_status("ongoing")).filter(task_package=task_package)
        else:
            tasks = Tasks.objects.filter(user_id=user.id).filter(business_type=business_type).filter(task_status=getenum_task_status("ongoing")).filter(task_package=task_package)

        serializer = self.serializer_class(tasks, many=True)
        split_variants = [v["task_ele"] for v in serializer.data]
        business_stage = serializer.data[0]["business_stage"]
        if business_stage == getenum_business_stage("init"):
            similar_parts_comp = "similar_parts_draft"
        elif business_stage == getenum_business_stage("review"):
            similar_parts_comp = "similar_parts_review"
        else:
            similar_parts_comp = "similar_parts_final"
        results = []
        staged_result = []
        key_list = {
            1: [
                "id",
                'skip_num_draft',
                'init_split_draft',
                'other_init_split_draft',
                'deform_split_draft',
                'similar_parts_draft',
                'dup_id_draft'
            ],
            2: [
                "id",
                'skip_num_review',
                'init_split_review',
                'other_init_split_review',
                'deform_split_review',
                'similar_parts_review',
                'dup_id_review'
            ],
            3: [
                "id",
                'skip_num_final',
                'init_split_final',
                'other_init_split_final',
                'deform_split_final',
                'similar_parts_final',
                'dup_id_final'
            ]
        }

        for split_variant in split_variants:
            if split_variant["source"] == int(source) and (hanzi_char in split_variant["hanzi_char"] or similar_parts in split_variant[similar_parts_comp]):
                results.append(split_variant)
        for result in results:
            tmp = {}
            for key in key_list[business_stage]:
                tmp[key] = result[key]
            staged_result.append(tmp)
        return_dict = {
            "task_package": int(task_package),
            "models": staged_result
        }

        return Response(return_dict)

    # 按页查看录入任务-进行中
    @list_route()
    def ongoing_inputpage(self, request, *args, **kwargs):
        user = self.request.user
        if self.request.query_params["task_package"]:
            task_package = self.request.query_params["task_package"]
        business_type = getenum_business_type("input_page")
        if user.is_superuser == 1:
            tasks = Tasks.objects.filter(business_type=business_type).filter(task_status=getenum_task_status("ongoing")).filter(task_package=task_package)
        else:
            tasks = Tasks.objects.filter(user_id=user.id).filter(business_type=business_type).filter(task_status=getenum_task_status("ongoing")).filter(task_package=task_package)

        serializer = self.serializer_class(tasks, many=True)
        input_pages = [v["task_ele"] for v in serializer.data]

        return_dict = {
            "task_package": int(task_package),
            "models": input_pages
        }

        return Response(return_dict)

    # 搜索录入任务
    @list_route()
    def select_input(self, request, *args, **kwargs):
        user = self.request.user
        hanzi_char = self.request.query_params["hanzi_char"]
        note = self.request.query_params["note"]
        task_package = self.request.query_params["task_package"]
        business_type = getenum_business_type("input")
        if user.is_superuser == 1:
            tasks = Tasks.objects.filter(business_type=business_type).filter(task_status=getenum_task_status("ongoing")).filter(task_package=task_package)
        else:
            tasks = Tasks.objects.filter(user_id=user.id).filter(business_type=business_type).filter(task_status=getenum_task_status("ongoing")).filter(task_package=task_package)

        serializer = self.serializer_class(tasks, many=True)
        input_variants = [v["task_ele"] for v in serializer.data]
        business_stage = serializer.data[0]["business_stage"]
        if business_stage == getenum_business_stage("init"):
            hanzi_char_comp = "hanzi_char_draft"
            variant_type_comp = "variant_type_draft"
            notes_comp = "notes_draft"
        elif business_stage == getenum_business_stage("review"):
            hanzi_char_comp = "hanzi_char_review"
            variant_type_comp = "variant_type_review"
            notes_comp = "notes_review"
        else:
            hanzi_char_comp = "hanzi_char_final"
            variant_type_comp = "variant_type_final"
            notes_comp = "notes_final"
        staged_result = []
        key_list = {
            1: [
                "id",
                'page_num',
                'seq_num_draft',
                'hanzi_char_draft',
                'hanzi_pic_id_draft',
                'variant_type_draft',
                'std_hanzi_draft',
                'notes_draft',
                'is_del_draft'
            ],
            2: [
                "id",
                'page_num',
                'seq_num_review',
                'hanzi_char_review',
                'hanzi_pic_id_review',
                'variant_type_review',
                'std_hanzi_review',
                'notes_review',
                'is_del_review'
            ],
            3: [
                "id",
                'page_num',
                'seq_num_final',
                'hanzi_char_final',
                'hanzi_pic_id_final',
                'variant_type_final',
                'std_hanzi_final',
                'notes_final',
                'is_del_final'
            ]
        }

        if self.request.query_params["page_num"]:
            page_num = int(self.request.query_params["page_num"])
            input_variants = [input_variant for input_variant in input_variants if page_num == input_variant["page_num"]]
        if self.request.query_params["variant_type"]:
            variant_type = int(self.request.query_params["variant_type"])
            input_variants = [input_variant for input_variant in input_variants if variant_type == input_variant[variant_type_comp]]
        if note:
            input_variants = [input_variant for input_variant in input_variants if note in str(input_variant[notes_comp])]
        if hanzi_char:
            input_variants = [input_variant for input_variant in input_variants if hanzi_char in input_variant[hanzi_char_comp]]

        for result in input_variants:
            tmp = {}
            for key in key_list[business_stage]:
                tmp[key] = result[key]
            staged_result.append(tmp)
        return_dict = {
            "business_stage": business_stage,
            "task_package": int(task_package),
            "models": staged_result
        }

        return Response(return_dict)

    # 按字头查看高台去重任务-进行中
    @list_route()
    def ongoing_dedup(self, request, *args, **kwargs):
        user = self.request.user
        task_package = request.query_params["task_package"]
        business_type = getenum_business_type("dedup")
        if user.is_superuser == 1:
            tasks = Tasks.objects.filter(business_type=business_type).filter(task_status=getenum_task_status("ongoing")).filter(task_package=task_package)
        else:
            tasks = Tasks.objects.filter(user_id=user.id).filter(business_type=business_type).filter(task_status=getenum_task_status("ongoing")).filter(task_package=task_package)

        serializer = self.serializer_class(tasks, many=True)
        dedup_variants = [v["task_ele"] for v in serializer.data]
        return_dict = {
            "task_package": int(task_package),
            "models": dedup_variants
        }

        return Response(return_dict)

    # 太难跳过，仅拆字
    @detail_route(methods=["PATCH", "GET", "PUT"])
    def skip_task(self, request, *args, **kwargs):
        origin_task = self.get_object()
        work_ele = origin_task.content_object

        business_type = origin_task.business_type
        business_stage = origin_task.business_stage
        user = origin_task.user
        task_package = origin_task.task_package

        if business_stage == getenum_business_stage("init"):
            work_ele.skip_num_draft += 1
        elif business_stage == getenum_business_stage("review"):
            work_ele.skip_num_review += 1
        else:
            work_ele.skip_num_final += 1
        work_ele.save()
        reset_task(origin_task)

        new_task = assign_task(business_type, business_stage, task_package, user)
        if new_task:
            serializer = api_variants_split.VariantsSplitSerializer(new_task.content_object)
            return Response(serializer.data)
        else:
            return Response(_("No more task today, have a try tommorrow!"), status=status.HTTP_204_NO_CONTENT)

    @list_route()
    def split_search(self, request, *args, **kwargs):
        hanzi_char = request.query_params.get('hanzi_char', False)
        hanzi_pic_id = request.query_params.get('hanzi_pic_id', False)

        if hanzi_char:
            qs_split = VariantsSplit.objects.filter(hanzi_char=hanzi_char)
        elif hanzi_pic_id:
            qs_split = VariantsSplit.objects.filter(hanzi_pic_id=hanzi_pic_id)
        else:
            qs_split = None

        if qs_split is None:
            return HttpResponseNotFound(_("Not found for specific char %s(%s)." % (hanzi_char, hanzi_pic_id)))

        # Here we assume that query result only has 1 item because hanzi_char is unique in code.
        # But there isn't any assurance in code defence to guarantee that.
        if qs_split.count() > 1:
            raise MultipleObjectsReturned(_("Multiple objects returned for specific char %s(%s)." % (hanzi_char, hanzi_pic_id)))

        business_id = qs_split[0].id

        qs = Tasks.objects.filter(business_type=getenum_business_type('split')).filter(object_id=business_id)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @list_route()
    def input_search(self, request, *args, **kwargs):
        hanzi_char = request.query_params.get('hanzi_char', False)
        hanzi_pic_id = request.query_params.get('hanzi_pic_id', False)
        page_num = request.query_params.get('page_num', False)
        notes = request.query_params.get('notes', False)

        sql = '''
            select lq_tasks.id from lq_tasks
            join lq_variants_input on lq_tasks.`object_id` = lq_variants_input.id
            where lq_tasks.`business_type` = %d
        ''' % (getenum_business_type('input'))

        if hanzi_char:
            sql += ' and (lq_variants_input.hanzi_char_draft = "%s" or lq_variants_input.hanzi_char_review= "%s" or lq_variants_input.hanzi_char_final = "%s")' % (hanzi_char, hanzi_char, hanzi_char)
        elif hanzi_pic_id:
            sql += ' and (lq_variants_input.hanzi_pic_id_draft = "%s" or lq_variants_input.hanzi_pic_id_review= "%s" or lq_variants_input.hanzi_pic_id_final = "%s")' % (
                hanzi_pic_id, hanzi_pic_id, hanzi_pic_id)

        if page_num:
            sql += ' and lq_variants_input.page_num = %d' % int(page_num)

        if notes:
            sql += ' and (lq_variants_input.notes_draft like "%%%%%s%%%%" or lq_variants_input.notes_review like "%%%%%s%%%%" or lq_variants_input.notes_final like "%%%%%s%%%%")' % (
                notes, notes, notes)

        qs = Tasks.objects.raw(sql)
        qslist = list(qs)
        qs.count = lambda: len(qslist)
        RawQuerySet.__getitem__ = lambda this, k: qslist

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @list_route()
    def dedup_search(self, request, *args, **kwargs):
        hanzi_char = request.query_params.get('hanzi_char', False)

        sql = '''
                 select lq_tasks.id from lq_tasks
                 join lq_inter_dict_dedup on lq_tasks.`object_id` = lq_inter_dict_dedup.id
                 where lq_tasks.`business_type` = %d and lq_inter_dict_dedup.std_hanzi = "%s"
             ''' % (getenum_business_type('dedup'), hanzi_char)

        qs = Tasks.objects.raw(sql)
        qslist = list(qs)
        qs.count = lambda: len(qslist)
        RawQuerySet.__getitem__ = lambda this, k: qslist

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
