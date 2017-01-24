# -*- coding:utf8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from backend.models import VARIANT_TYPE_CHOICES, HANZI_TYPE_CHOICES, SOURCE_CHOICES, BUSINESS_STAGE_CHOICES


@login_required
def lq_hanzi_db_search(request):
    if request.user.is_staff == 1:
        return render(request, 'lq_hanzi_db_search.html',
                      {
                          "variant_type_choices": VARIANT_TYPE_CHOICES,
                          "hanzi_type_choices": HANZI_TYPE_CHOICES,
                          "source_choices": SOURCE_CHOICES
                      })
    return HttpResponse('Unauthorized', status=401)


@login_required
def lq_split_db_search(request):
    if request.user.is_staff == 1:
        return render(request, 'lq_split_db_search.html',
                      {
                          "source_choices": SOURCE_CHOICES,
                          "business_stage_choices": BUSINESS_STAGE_CHOICES
                      })
    return HttpResponse('Unauthorized', status=401)


@login_required
def cn_dict_input_db_search(request):
    if request.user.is_staff == 1:
        return render(request, 'cn_dict_input_db_search.html')
    return HttpResponse('Unauthorized', status=401)


@login_required
def cn_dict_dedup_db_search(request):
    if request.user.is_staff == 1:
        return render(request, 'cn_dict_dedup_db_search.html')
    return HttpResponse('Unauthorized', status=401)


@login_required
def korean_dedup_db_search(request):
    if request.user.is_staff == 1:
        return render(request, 'korean_dedup_db_search.html')
    return HttpResponse('Unauthorized', status=401)


@login_required
def korean_taiwan_dedup_db_search(request):
    if request.user.is_staff == 1:
        return render(request, 'korean_taiwan_dedup_db_search.html')
    return HttpResponse('Unauthorized', status=401)
