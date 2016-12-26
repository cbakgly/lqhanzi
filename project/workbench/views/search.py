# -*- coding:utf8 -*-
from django.shortcuts import render


def lq_hanzi_db_search(request):
    return render(request, 'lq_hanzi_db_search.html')


def lq_split_db_search(request):
    return render(request, 'lq_split_db_search.html')


def cn_dict_input_db_search(request):
    return render(request, 'cn_dict_input_db_search.html')


def cn_dict_dedup_db_search(request):
    return render(request, 'cn_dict_dedup_db_search.html')


def korean_dedup_db_search(request):
    return render(request, 'korean_dedup_db_search.html')


def korean_taiwan_dedup_db_search(request):
    return render(request, 'korean_taiwan_dedup_db_search.html')