# -*- coding:utf8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from backend.models import KoreanDupCharacters, HanziSet, InterDictDedup
from backend.enums import getenum_source
from backend.views.api_hanzi_set import HanziSetDedupSerializer
from backend.views.api_variants_dedup import InterDictDedupSerializer

@login_required
def task_split(request):
    return render(request, 'task_split.html')


@login_required
def task_input(request):
    return render(request, 'task_input.html')


@login_required
def task_dedup(request, *args, **kwargs):
    pk = int(kwargs["pk"])
    dedup_character = list(KoreanDupCharacters.objects.filter(pk=pk))[0]
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
                   'taiwan_list': taiwan_list
                   })
