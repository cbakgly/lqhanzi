# -*- coding:utf8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def lq_hanzi_db_search(request):
    return render(request, 'lq_hanzi_db_search.html')


@login_required
def lq_split_db_search(request):
    return render(request, 'lq_split_db_search.html')


@login_required
def cn_dict_input_db_search(request):
    return render(request, 'cn_dict_input_db_search.html')


@login_required
def cn_dict_dedup_db_search(request):
    return render(request, 'cn_dict_dedup_db_search.html')


@login_required
def korean_dedup_db_search(request):
    return render(request, 'korean_dedup_db_search.html')


@login_required
def korean_taiwan_dedup_db_search(request):
    return render(request, 'korean_taiwan_dedup_db_search.html')