# -*- coding:utf8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from backend.models import HanziSet, InterDictDedup, Tasks, VariantsInput, INPUT_VARIANT_TYPE_CHOICES
from backend.enums import getenum_source, getenum_task_status, getenum_business_type
from backend.views.api_hanzi_set import HanziSetDedupSerializer
from backend.views.api_variants_dedup import InterDictDedupSerializer
from backend.utils import has_business_type_perm


@login_required
def task_split(request, *args, **kwargs):
    if not has_business_type_perm(request.user, 'split'):
        return render(request, '401.html')

    if request.GET.get('id') is not None:
        return render(request, 'task_split_view.html', {'char_id': request.GET.get('id')})

    return render(request, 'task_split.html', {'task_package_id': request.GET.get('pk')})


@login_required
def task_input(request, *args, **kwargs):
    if has_business_type_perm(request.user, 'input'):
        pk = int(kwargs["pk"])
        task = list(Tasks.objects.filter(business_type=9, task_package_id=pk, task_status=getenum_task_status("ongoing")))
        if task:
            task = task[0]
            input_page = task.content_object
            inputs = VariantsInput.objects.filter(page_num=input_page.page_num)

            return render(request, 'task_input.html',
                          {
                              'inputpage': input_page,
                              'inputs': inputs,
                              'task_package_id': request.GET.get('pk'),
                              'business_stage': task.business_stage,
                              'input_variant_type': INPUT_VARIANT_TYPE_CHOICES
                          })
    return render(request, '401.html')


@login_required
def task_dedup(request, *args, **kwargs):
    if not has_business_type_perm(request.user, 'dedup'):
        return render(request, '401.html')

    pk = int(kwargs["pk"])
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
def task_dedup2(request, *args, **kwargs):
    if not has_business_type_perm(request.user, 'dedup'):
        return render(request, '401.html')

    pk = int(request.GET.get('pk'))
    task = list(Tasks.objects.filter(task_package_id=pk, task_status=getenum_task_status("ongoing")))
    if task:
        task = task[0]
        dedup_character = task.content_object

        korean_list = InterDictDedupSerializer(InterDictDedup.objects.filter(std_hanzi=dedup_character.korean_variant).filter(source=getenum_source('korean')), many=True).data
        korean_char = dedup_character.korean_variant

        if dedup_character.relation is 3:
            taiwan_list = HanziSetDedupSerializer(HanziSet.objects.filter(std_hanzi=dedup_character.unicode).filter(source=getenum_source('taiwan')), many=True).data
            taiwan_char = dedup_character.unicode
        else:
            taiwan_list = HanziSetDedupSerializer(HanziSet.objects.filter(std_hanzi=dedup_character.korean_variant).filter(source=getenum_source('taiwan')), many=True).data
            taiwan_char = dedup_character.korean_variant

        return render(request, 'task_dedup2.html',
                      {'korean_char': korean_char,
                       'korean_list': korean_list,
                       'taiwan_char': taiwan_char,
                       'taiwan_list': taiwan_list,
                       'task_package_id': pk,
                       'business_stage': task.business_stage,
                       'korean_dedup_id': dedup_character.id
                       })


@login_required
def credit_redeem(request, *args, **kwargs):
    user = request.user
