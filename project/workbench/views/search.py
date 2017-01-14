# -*- coding:utf8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from backend.models import variant_type_choices, hanzi_type_choices, source_choices, business_stage_choices


@login_required
def lq_hanzi_db_search(request):
    if request.user.is_staff == 1:
        return render(request, 'lq_hanzi_db_search.html',
                      {
                          "variant_type_choices": variant_type_choices,
                          "hanzi_type_choices": hanzi_type_choices,
                          "source_choices": source_choices
                      })
    return HttpResponse('Unauthorized', status=401)


@login_required
def lq_split_db_search(request):
    if request.user.is_staff == 1:
        return render(request, 'lq_split_db_search.html',
                      {
                          "source_choices": source_choices,
                          "business_stage_choices": business_stage_choices
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
