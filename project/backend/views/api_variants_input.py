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
from ..models import VariantsInput, InputPage
from ..filters import NumberInFilter
from ..enums import getenum_task_status, getenum_business_stage, getenum_business_type, getenum_source
from task_func import assign_task
from ..utils import get_pic_url_by_source_pic_name, get_input_page_path
from ..auth import IsBusinessMember


def update_tasks_status(variants_input):
    tasks = list(variants_input.task.all())
    task_dict = {}
    for t in tasks:
        task_dict[t.business_stage] = t
    draft = task_dict[getenum_business_stage('init')]
    review = task_dict[getenum_business_stage('review')]
    final = task_dict[getenum_business_stage('final')]
    origin_task = draft
    if draft.task_status == getenum_task_status("ongoing"):
        draft.task_status = getenum_task_status("completed")
        draft.completed_at = timezone.now()
        review.task_status = getenum_task_status("to_be_arranged")
        variants_input.save()
        draft.save()
        review.save()
    elif review.task_status == getenum_task_status("ongoing"):
        review.task_status = getenum_task_status("completed")
        review.completed_at = timezone.now()
        final.task_status = getenum_task_status("to_be_arranged")
        variants_input.is_draft_equals_review = variants_input.hanzi_char_draft is variants_input.hanzi_char_review
        variants_input.save()
        review.save()
        final.save()
        origin_task = review
    elif final.task_status == getenum_task_status("ongoing"):
        final.task_status = getenum_task_status("completed")
        final.completed_at = timezone.now()
        variants_input.is_review_equals_final = variants_input.hanzi_char_review is variants_input.hanzi_char_final
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
        ret['hanzi_pic_path_draft'] = get_pic_url_by_source_pic_name(getenum_source('hanyu'), ret['hanzi_pic_id_draft'])
        ret['hanzi_pic_path_review'] = get_pic_url_by_source_pic_name(getenum_source('hanyu'), ret['hanzi_pic_id_review'])
        ret['hanzi_pic_path_final'] = get_pic_url_by_source_pic_name(getenum_source('hanyu'), ret['hanzi_pic_id_final'])
        ret['variant_type_draft'] = instance.get_variant_type_draft_display()
        ret['variant_type_review'] = instance.get_variant_type_review_display()
        ret['variant_type_final'] = instance.get_variant_type_final_display()
        ret['is_del_draft'] = instance.get_is_del_draft_display()
        ret['is_del_review'] = instance.get_is_del_review_display()
        ret['is_del_final'] = instance.get_is_del_final_display()
        ret['is_draft_equals_review_display'] = instance.get_is_draft_equals_review_display()
        ret['is_review_equals_final_display'] = instance.get_is_review_equals_final_display()
        ret['is_checked_display'] = instance.get_is_checked_display()
        ret['is_submitted_display'] = instance.get_is_submitted_display()
        return ret


class VariantsDraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = VariantsInput
        fields = [
            "id",
            'page_num',
            'seq_num_draft',
            'hanzi_char_draft',
            'hanzi_pic_id_draft',
            'variant_type_draft',
            'std_hanzi_draft',
            'notes_draft',
            'is_del_draft'
        ]
        depth = 0


class VariantsReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = VariantsInput
        fields = [
            "id",
            'page_num',
            'seq_num_draft',
            'hanzi_char_draft',
            'hanzi_pic_id_draft',
            'variant_type_draft',
            'std_hanzi_draft',
            'notes_draft',
            'is_del_draft',
            'seq_num_review',
            'hanzi_char_review',
            'hanzi_pic_id_review',
            'variant_type_review',
            'std_hanzi_review',
            'notes_review',
            'is_del_review'
        ]
        depth = 0


class VariantsFinalSerializer(serializers.ModelSerializer):

    class Meta:
        model = VariantsInput
        fields = [
            "id",
            'page_num',
            'seq_num_draft',
            'hanzi_char_draft',
            'hanzi_pic_id_draft',
            'variant_type_draft',
            'std_hanzi_draft',
            'notes_draft',
            'is_del_draft',
            'seq_num_review',
            'hanzi_char_review',
            'hanzi_pic_id_review',
            'variant_type_review',
            'std_hanzi_review',
            'notes_review',
            'is_del_review',
            'seq_num_final',
            'hanzi_char_final',
            'hanzi_pic_id_final',
            'variant_type_final',
            'std_hanzi_final',
            'notes_final',
            'is_del_final'
        ]
        depth = 0


class VariantsInputFilter(django_filters.FilterSet):

    """
    异体字拆字过滤器
    """
    business_type_in = NumberInFilter(name='business_type', lookup_expr='in')

    class Meta:
        model = VariantsInput
        fields = "__all__"


class VariantsInputViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsBusinessMember)
    filter_class = VariantsInputFilter
    pagination_class = NumberPagination
    serializer_class = VariantsInputSerializer
    queryset = VariantsInput.objects.all()

    # 单个录入任务提交
    @detail_route(methods=["PUT", "GET", "PATCH"])
    def submit_single_input(self, request, *args, **kwargs):
        variants_input = self.get_object()
        stage = request.data['stage']
        serializer = VariantsInputSerializer(data=request.data)
        data = serializer.initial_data
        if stage == "first":
            variants_input.variant_type_draft = data['variant_type']
            variants_input.std_hanzi_draft = data['std_hanzi']
            variants_input.notes_draft = data['notes']
        elif stage == 'review':
            variants_input.variant_type_review = data['variant_type']
            variants_input.std_hanzi_review = data['std_hanzi']
            variants_input.notes_review = data['notes']
        else:
            variants_input.variant_type_final = data['variant_type']
            variants_input.std_hanzi_final = data['std_hanzi']
            variants_input.notes_final = data['notes']

        variants_input.save()
        tasks = list(variants_input.task.all())
        for t in tasks:
            if t.task_status == getenum_task_status("ongoing"):
                t.save()
                break
        return Response(VariantsInputSerializer(variants_input).data)

    # 插入新行
    @detail_route(methods=["GET", "PUT", "PATCH"])
    def insert_new_line(self, request, *args, **kwargs):
        variants_input = self.get_object()
        page_num = variants_input.page_num
        business_stage = request.query_params["business_stage"]
        new_input = VariantsInput(page_num=page_num)
        new_input.save()
        if business_stage is getenum_business_stage('init'):
            inputs = list(VariantsInput.objects.filter(page_num=page_num, seq_num_draft__gt=variants_input.seq_num_draft).order_by('seq_num_draft'))
            for input in inputs:
                input.seq_num_draft += 1
                input.save()
        elif business_stage is getenum_business_stage('review'):
            inputs = list(VariantsInput.objects.filter(page_num=page_num, seq_num_review__gt=variants_input.seq_num_review).order_by('seq_num_review'))
            for input in inputs:
                input.seq_num_review += 1
                input.save()
        else:
            inputs = list(VariantsInput.objects.filter(page_num=page_num, seq_num_final__gt=variants_input.seq_num_final).order_by('seq_num_final'))
            for input in inputs:
                input.seq_num_final += 1
                input.save()
        return Response(VariantsInputSerializer(new_input).data)

    # 删除行
    @detail_route(methods=["GET", "PUT", "PATCH"])
    def del_input(self, request, *args, **kwargs):
        variants_input = self.get_object()
        business_stage = request.query_params["business_stage"]
        if business_stage is getenum_business_stage('init'):
            variants_input.is_del_draft = True
        elif business_stage is getenum_business_stage('review'):
            variants_input.is_del_review = True
        else:
            variants_input.is_del_final = True
        variants_input.save()
        return Response(VariantsInputSerializer(variants_input).data)

    # 回查 审查 的查看功能
    @detail_route(methods=["GET", "PUT", "PATCH"])
    def view_info(self, request, *args, **kwargs):
        variants_input = self.get_object()
        business_stage = int(request.query_params["business_stage"])

        if business_stage is getenum_business_stage('init'):
            return Response(VariantsDraftSerializer(variants_input).data)
        elif business_stage is getenum_business_stage('review'):
            return Response(VariantsReviewSerializer(variants_input).data)
        else:
            return Response(VariantsFinalSerializer(variants_input).data)


class InputPageSerializer(serializers.ModelSerializer):
    variant_inputs = serializers.SerializerMethodField()

    class Meta:
        model = InputPage
        fields = "__all__"

    def get_variant_inputs(self, obj):
        inputs = VariantsInput.objects.filter(page_num=obj.page_num)
        return VariantsInputSerializer(inputs, many=True).data


class InputPageFilter(django_filters.FilterSet):

    """
    异体字拆字过滤器
    """

    class Meta:
        model = InputPage
        fields = "__all__"


def update_status(inputpage):
    tasks = list(inputpage.task.all())
    task_dict = {}
    for t in tasks:
        task_dict[t.business_stage] = t
    draft = task_dict[getenum_business_stage('init')]
    review = task_dict[getenum_business_stage('review')]
    final = task_dict[getenum_business_stage('final')]
    origin_task = draft
    if draft.task_status == getenum_task_status("ongoing"):
        draft.task_status = getenum_task_status("completed")
        draft.completed_at = timezone.now()
        review.task_status = getenum_task_status("to_be_arranged")
        inputpage.save()
        draft.save()
        review.save()
    elif review.task_status == getenum_task_status("ongoing"):
        review.task_status = getenum_task_status("completed")
        review.completed_at = timezone.now()
        final.task_status = getenum_task_status("to_be_arranged")
        inputpage.save()
        review.save()
        final.save()
        origin_task = review
    elif final.task_status == getenum_task_status("ongoing"):
        final.task_status = getenum_task_status("completed")
        final.completed_at = timezone.now()
        inputpage.save()
        final.save()
        origin_task = final
    else:
        pass
    return origin_task


class InputPageViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsBusinessMember)

    queryset = InputPage.objects.all()
    filter_class = InputPageFilter
    pagination_class = NumberPagination
    serializer_class = InputPageSerializer

    # 提交并转下一页
    @detail_route(methods=["PUT", "GET", "PATCH"])
    def submit_and_next(self, request, *args, **kwargs):
        input_page = self.get_object()

        origin_task = update_status(input_page)
        task_package = origin_task.task_package
        task_plan = task_package.size
        task_num = len(list(task_package.tasks.all()))
        if task_num < task_plan:
            business_stage = origin_task.business_stage
            user = origin_task.user
            new_task = assign_task(getenum_business_type("input_page"), business_stage, task_package, user)
            if new_task:
                id = new_task.object_id
                return Response(id)
            else:
                return Response(_("No more task today, have a try tommorrow!"), status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(_("This package is completed, please apply for a new one!"), status=status.HTTP_100_CONTINUE)

    # 提交当前页
    @detail_route(methods=["PUT", "GET", "PATCH"])
    def submit(self, request, *args, **kwargs):
        input_page = self.get_object()
        origin_task = update_tasks_status(input_page)

        task_package = origin_task.task_package
        task_plan = task_package.size
        task_num = len(list(task_package.tasks.all()))
        if task_num < task_plan:
            return Response(_("Thanks for working, the package is not finished yet, please carry on!"), status=status.HTTP_100_CONTINUE)
        else:
            return Response(_("This package is completed, please apply for a new one!"), status=status.HTTP_303_SEE_OTHER)

    @detail_route(methods=["GET"])
    def next_page(self, request, *args, **kwargs):
        if 'pk' in kwargs.keys():
            pk = kwargs['pk']
        else:
            pk = request.GET['pk']
        next_page = list(InputPage.objects.filter(page_num__gt=pk).order_by('page_num'))[0]

        return Response({"next_page": next_page.page_num})

    @detail_route(methods=["GET"])
    def last_img(self, request, *args, **kwargs):
        if 'pk' in kwargs.keys():
            pk = kwargs['pk']
        else:
            pk = request.GET['pk']
        page_num = int(pk) - 1
        if page_num:
            path = get_input_page_path(page_num)
        else:
            path = ""

        return Response({"last_img": path})

    @detail_route(methods=["GET"])
    def next_img(self, request, *args, **kwargs):
        if 'pk' in kwargs.keys():
            pk = kwargs['pk']
        else:
            pk = request.GET['pk']
        page_num = int(pk) + 1
        if page_num:
            path = get_input_page_path(page_num)
        else:
            path = ""

        return Response({"next_img": path})
