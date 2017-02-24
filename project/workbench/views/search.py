# -*- coding:utf8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from backend.models import VARIANT_TYPE_CHOICES, HANZI_TYPE_CHOICES, SOURCE_CHOICES, BUSINESS_STAGE_CHOICES
from backend.utils import has_workbench_perm, has_business_type_perm


@login_required
def lq_hanzi_db_search(request):
    if has_workbench_perm(request.user):
        return render(request, 'lq_hanzi_db_search.html',
                      {
                          "variant_type_choices": VARIANT_TYPE_CHOICES,
                          "hanzi_type_choices": HANZI_TYPE_CHOICES,
                          "source_choices": SOURCE_CHOICES
                      })
    return render(request, '401.html')


@login_required
def lq_split_db_search(request):
    if has_business_type_perm(request.user, 'split'):
        return render(request, 'lq_split_db_search.html',
                      {
                          "source_choices": SOURCE_CHOICES,
                          "business_stage_choices": BUSINESS_STAGE_CHOICES
                      })
    return render(request, '401.html')


@login_required
def cn_dict_input_db_search(request):
    if has_business_type_perm(request.user, 'input'):
        return render(request, 'cn_dict_input_db_search.html')
    return render(request, '401.html')


@login_required
def cn_dict_dedup_db_search(request):
    if has_business_type_perm(request.user, 'dedup'):
        return render(request, 'cn_dict_dedup_db_search.html')
    return render(request, '401.html')


@login_required
def korean_dedup_db_search(request):
    if has_business_type_perm(request.user, 'dedup'):
        return render(request, 'korean_dedup_db_search.html')
    return render(request, '401.html')


@login_required
def korean_taiwan_dedup_db_search(request):
    if has_business_type_perm(request.user, 'dedup'):
        return render(request, 'korean_taiwan_dedup_db_search.html')
    return render(request, '401.html')

