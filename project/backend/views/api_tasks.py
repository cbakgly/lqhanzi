# encoding: utf-8
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import django_filters
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from django.core.exceptions import MultipleObjectsReturned
from django.db.models.query import RawQuerySet

from api_variants_input import VariantsInputSerializer, InputPageSerializer
from api_variants_dedup import InterDictDedupSerializer
from api_variants_split import VariantsSplitSerializer
from api_korean_dup_characters import KoreanDupCharactersSerializer
from api_variants_korean_dedup import KoreanDedupSerializer
from api_hanzi_set import HanziSetDedupSerializer
from task_func import assign_task, reset_task, get_working_task
from ..pagination import NumberPagination
from ..models import Tasks, VariantsSplit, KoreanDedup, VariantsInput, KoreanDupCharacters, InputPage, TaskPackages, InterDictDedup, HanziSet
from ..enums import getenum_business_type, getenum_business_stage, getenum_source
from ..auth import IsBusinessMember
from ..utils import has_business_type_perm


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
            ele_serializer = VariantsInputSerializer
        elif isinstance(task_ele, VariantsSplit):
            ele_serializer = VariantsSplitSerializer
        elif isinstance(task_ele, KoreanDedup):
            ele_serializer = KoreanDedupSerializer
        elif isinstance(task_ele, KoreanDupCharacters):
            ele_serializer = KoreanDupCharactersSerializer
        elif isinstance(task_ele, InputPage):
            ele_serializer = InputPageSerializer
        else:
            ele_serializer = InterDictDedupSerializer

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
    permission_classes = (IsAuthenticated, IsBusinessMember)
    pagination_class = NumberPagination
    serializer_class = TasksSerializer
    filter_class = TasksFilter

    def get_queryset(self):
        user = self.request.user
        qs = Tasks.objects.filter(user_id=user.id)
        return qs

    @list_route()
    def ongoing_split(self, request, *args, **kwargs):
        """
        列出当前进行中的拆字任务
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        user = self.request.user
        if not has_business_type_perm(user, 'split'):
            return HttpResponseForbidden(_("You don't have permission to view."))

        task_package_id = request.query_params.get("task_package_id", 0)
        if task_package_id == 0:
            return HttpResponseBadRequest(_("ID invalid."))

        task_package = TaskPackages.objects.get(pk=task_package_id)

        task = get_working_task(task_package, user)
        if not task:
            task = assign_task(task_package.business_type, task_package.business_stage, task_package, user)

        if task:
            serializer = self.get_serializer([task], many=True)
            return Response(serializer.data)

        return Response({"error": _("No more task today, have a try tommorrow!")}, status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=["PATCH", "GET", "PUT"])
    def submit_split(self, request, *args, **kwargs):
        pass

    @detail_route(methods=["PATCH", "GET", "PUT"])
    def submit_next_split(self, request, *args, **kwargs):
        """
        提交并返回下一条任务数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if not has_business_type_perm(request.user, 'split'):
            return HttpResponseForbidden(_("You don't have permission to view."))

        business_stage = request.data['business_stage']
        business_type = request.data['business_type']
        task = Tasks.objects.get(pk=request.data['id'])
        split = task.content_object

        if business_stage == getenum_business_stage('init'):
            if request.data['task_ele']['dup_id_draft'] != '':
                split.dup_id_draft = request.data['task_ele']['dup_id_draft']
            else:
                split.init_split_draft = request.data['task_ele']['init_split_draft']
                split.other_init_split_draft = request.data['task_ele']['other_init_split_draft']
                split.deform_split_draft = request.data['task_ele']['deform_split_draft']
                split.similar_parts_draft = request.data['task_ele']['similar_parts_draft']
        elif business_stage == getenum_business_stage('review'):
            if request.data['task_ele']['dup_id_review'] != '':
                split.dup_id_review = request.data['task_ele']['dup_id_review']
            else:
                split.init_split_review = request.data['task_ele']['init_split_review']
                split.other_init_split_review = request.data['task_ele']['other_init_split_review']
                split.deform_split_review = request.data['task_ele']['deform_split_review']
                split.similar_parts_review = request.data['task_ele']['similar_parts_review']
        elif business_stage == getenum_business_stage('final'):
            if request.data['task_ele']['dup_id_final'] != '':
                split.dup_id_final = request.data['task_ele']['dup_id_final']
            else:
                split.init_split_final = request.data['task_ele']['init_split_final']
                split.other_init_split_final = request.data['task_ele']['other_init_split_final']
                split.deform_split_final = request.data['task_ele']['deform_split_final']
                split.similar_parts_final = request.data['task_ele']['similar_parts_final']
        split.save()

        new_task = assign_task(business_type, business_stage, task.task_package, task.user)

        if new_task:
            serializer = self.get_serializer([new_task], many=True)
            return Response(serializer.data)
        else:
            return Response({"error": _("No more task today, have a try tommorrow!")}, status=status.HTTP_204_NO_CONTENT)

    @detail_route(methods=["PATCH", "GET", "PUT"])
    def skip_task(self, request, *args, **kwargs):
        """
        太难跳过当前任务, 返回下一条
        目前只拆字用
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if not has_business_type_perm(request.user, 'split'):
            return HttpResponseForbidden(_("You don't have permission to view."))

        origin_task = Tasks.objects.get(pk=kwargs['pk'])
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

        new_task = assign_task(business_type, business_stage, task_package, user)
        reset_task(origin_task)

        if new_task:
            serializer = self.get_serializer([new_task], many=True)
            return Response(serializer.data)
        else:
            return Response({"error": _("No more task today, have a try tommorrow!")}, status=status.HTTP_204_NO_CONTENT)

    @list_route()
    def split_search(self, request, *args, **kwargs):
        """
        拆字任务包内容查看
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if not has_business_type_perm(request.user, 'split'):
            return HttpResponseForbidden(_("You don't have permission to view."))

        hanzi_char = request.query_params.get('hanzi_char', False)
        hanzi_pic_id = request.query_params.get('hanzi_pic_id', False)

        if hanzi_char:
            qs_split = VariantsSplit.objects.filter(user=request.user).filter(hanzi_char=hanzi_char)
        elif hanzi_pic_id:
            qs_split = VariantsSplit.objects.filter(user=request.user).filter(hanzi_pic_id=hanzi_pic_id)
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
        """
        录入任务包内容查看
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        if not has_business_type_perm(request.user, 'input'):
            return HttpResponseForbidden(_("You don't have permission to view."))

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
        """
        去重任务包内容查看
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if not has_business_type_perm(request.user, 'dedup'):
            return HttpResponseForbidden(_("You don't have permission to view."))

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


    @detail_route()
    def task_dedup_inter(self, request, *args, **kwargs):
        user = request.user
        if not has_business_type_perm(request.user, 'dedup'):
            return Response("!!!")

        if 'pk' in kwargs.keys():
            pk = kwargs['pk']
        else:
            pk = request.GET['pk']
        inter_dict = InterDictDedup.objects.get(pk=pk)
        std_hanzi = inter_dict.std_hanzi
        dedup_character = list(KoreanDupCharacters.objects.filter(korean_variant=std_hanzi))[0]

        korean_list = InterDictDedupSerializer(InterDictDedup.objects.filter(std_hanzi=dedup_character.korean_variant).filter(source=getenum_source('korean')), many=True).data
        korean_char = dedup_character.korean_variant

        if dedup_character.relation is 3:
            taiwan_list = HanziSetDedupSerializer(HanziSet.objects.filter(std_hanzi=dedup_character.unicode).filter(source=getenum_source('taiwan')), many=True).data
            taiwan_char = dedup_character.unicode
        else:
            taiwan_list = HanziSetDedupSerializer(HanziSet.objects.filter(std_hanzi=dedup_character.korean_variant).filter(source=getenum_source('taiwan')), many=True).data
            taiwan_char = dedup_character.korean_variant

        task = Tasks.objects.filter(user=user, object_id=dedup_character.id)
        if task:
            task = list(task)[0]

            return Response({'korean_char': korean_char,
                             'korean_list': korean_list,
                             'taiwan_char': taiwan_char,
                             'taiwan_list': taiwan_list,
                             'task_package_id': task.task_package_id,
                             'business_stage': task.business_stage,
                             'korean_dedup_id': dedup_character.id
                             })
        else:
            return Response(_("Inputdata Error!"), status=status.HTTP_400_BAD_REQUEST)
