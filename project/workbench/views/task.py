# -*- coding:utf8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from backend.models import HanziSet, InterDictDedup, Tasks, VariantsInput, INPUT_VARIANT_TYPE_CHOICES, InputPage, KoreanDupCharacters
from backend.enums import getenum_source, getenum_task_status, getenum_business_type
from backend.views.api_hanzi_set import HanziSetDedupSerializer
from backend.views.api_variants_dedup import InterDictDedupSerializer
from backend.views.api_variants_input import VariantsInputSerializer
from backend.utils import has_business_type_perm, get_input_page_path


@login_required
def task_split(request, *args, **kwargs):
    if not has_business_type_perm(request.user, 'split'):
        return render(request, '401.html')

    if request.GET.get('id', 0):
        return render(request, 'task_split_view.html', {'char_id': request.GET.get('id')})

    return render(request, 'task_split.html', {'task_package_id': request.GET.get('pk', 0)})


@login_required
def task_input(request, *args, **kwargs):
    if not has_business_type_perm(request.user, 'input'):
        return render(request, '401.html')

    if 'pk' in kwargs.keys():
        pk = kwargs['pk']
    else:
        pk = request.GET['pk']
    task = list(Tasks.objects.filter(business_type=9, task_package_id=pk, task_status=getenum_task_status("ongoing")))
    if task:
        task = task[0]
    else:
        task = list(Tasks.objects.filter(business_type=9, task_package_id=pk))
        task = task[0]

    input_page = task.content_object
    inputs = VariantsInput.objects.filter(page_num=input_page.page_num)

    return render(request, 'task_input.html',
                  {
                      'page_path': get_input_page_path(input_page.page_num),
                      'inputpage': input_page,
                      'inputs': inputs,
                      'task_package_id': pk,
                      'business_stage': task.business_stage,
                      'input_variant_type': INPUT_VARIANT_TYPE_CHOICES
                  })


@login_required
def input_detail(request, *args, **kwargs):
    if 'pk' in kwargs.keys():
        pk = kwargs['pk']
    else:
        pk = request.GET['pk']
    input_object = VariantsInput.objects.get(pk=pk)

    input_page = InputPage.objects.get(pk=input_object.page_num)
    inputs = VariantsInput.objects.filter(page_num=input_page.page_num)

    return render(request, 'input_detail.html',
                  {
                      'page_path': get_input_page_path(input_page.page_num),
                      'inputpage': input_page,
                      'inputs': inputs,
                      'input_variant_type': INPUT_VARIANT_TYPE_CHOICES
                  })


@login_required
def input_page_detail(request, *args, **kwargs):
    if 'pk' in kwargs.keys():
        pk = kwargs['pk']
    else:
        pk = request.GET['pk']
    try:
        input_page = InputPage.objects.get(pk=pk)
    except InputPage.DoesNotExist:
        return render(request, '400.html')
    try:
        inputs = VariantsInput.objects.filter(page_num=input_page.page_num)
    except VariantsInput.DoesNotExist:
        return render(request, '400.html')

    return render(request, 'input_detail.html',
                  {
                      'page_path': get_input_page_path(input_page.page_num),
                      'inputpage': input_page,
                      'inputs': VariantsInputSerializer(inputs, many=True).data,
                      'input_variant_type': INPUT_VARIANT_TYPE_CHOICES
                  })


@login_required
def task_dedup(request, *args, **kwargs):
    if not has_business_type_perm(request.user, 'dedup'):
        return render(request, '401.html')

    pk = int(request.GET.get("pk", 0))
    task = list(Tasks.objects.filter(task_package_id=pk, task_status=getenum_task_status("ongoing")))
    if task:
        task = task[0]
    else:
        task = list(Tasks.objects.filter(task_package_id=pk, business_type=getenum_business_type('dedup')).order_by('u_t'))[-1]
    dedup_character = task.content_object

    korean_list = InterDictDedupSerializer(InterDictDedup.objects.filter(std_hanzi=dedup_character.korean_variant).filter(source=getenum_source('korean')), many=True).data
    korean_char = dedup_character.korean_variant

    if dedup_character.relation is 3:
        taiwan_list = HanziSetDedupSerializer(HanziSet.objects.filter(std_hanzi=dedup_character.unicode).filter(source=getenum_source('taiwan')), many=True).data
        taiwan_char = dedup_character.unicode
    else:
        taiwan_list = HanziSetDedupSerializer(HanziSet.objects.filter(std_hanzi=dedup_character.korean_variant).filter(source=getenum_source('taiwan')), many=True).data
        taiwan_char = dedup_character.korean_variant

    return render(request, 'task_dedup.html',
                  {'korean_char': korean_char,
                   'korean_list': korean_list,
                   'taiwan_char': taiwan_char,
                   'taiwan_list': taiwan_list,
                   'task_package_id': pk,
                   'business_stage': task.business_stage,
                   'korean_dedup_id': dedup_character.id
                   })


@login_required
def task_dedup_inter(request, *args, **kwargs):
    user = request.user

    if 'pk' in kwargs.keys():
        pk = kwargs['pk']
    else:
        pk = request.GET['pk']

    return render(request, 'task_dedup_inter.html',
                  {'path':'/api/v1/tasks/'+pk+'/task_dedup_inter/'
                   })
