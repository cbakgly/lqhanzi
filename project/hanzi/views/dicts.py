# coding=utf-8

import json
import re
from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response
from backend.utils import get_pic_url_by_source_pic_name
from backend.utils import get_dunhuang_dict_path
from backend.utils import get_hanyu_dict_path
from backend.models import HanziParts, HanziSet, HanziRadicals
from backend.enums import SOURCE_ENUM
from appendix_hanzi import fuluzi


def get_radicals(source):
    """
    取部首函数
    """
    source_to_db_filed_hash = {1: b'is_un_radical', 2: b'is_tw_radical', 3: b'is_zh_radical',
                               4: b'is_kr_radical', 5: b'is_dh_radical'}
    field = source_to_db_filed_hash.get(int(source), False)
    radicals = []
    if field:
        radicals = HanziRadicals.objects.filter(**{field: 1}).values('radical', 'strokes')

    return radicals


@csrf_exempt
def taiwan(request):
    # get radicals
    source = SOURCE_ENUM['taiwan']
    radicals = get_radicals(source)

    # trans radicals
    trans_hash = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二', '十三', '十四', '十五',
                  '十六', '十七', '十八', '十九', '二十']
    radical_dict = {}
    for item in radicals:
        key = int(item['strokes'])
        if key in radical_dict:
            radical_dict[key]['radicals'].append(item['radical'])
        else:
            radical_dict[key] = {
                'strokes': int(item['strokes']),
                'strokes_str': trans_hash[int(item['strokes'])] + '画',
                'radicals': [item['radical']]
            }
    content = {'radical_dict': radical_dict, 'dict_name': '台湾异体字字典'}

    return render(request, 'hanzi_dicts.html', context=content)


@csrf_exempt
def dicts_search(request):
    # 得到参数
    q = request.GET.get('q', None)
    source = request.GET.get('source', None)
    page_size = request.GET.get('page_size', None)
    page_num = request.GET.get('page_num', None)
    left_stroke = request.GET.get('left_stroke', None)

    source = int(source)
    page_size = int(page_size)
    page_num = int(page_num)
    left_stroke = int(left_stroke)

    radical_strokes_num = Radical.objects.get(radical=q).strokes  # 部首笔画数

    if (left_stroke == -1):
        total = HanziSet.objects.filter(Q(radical=q) & Q(source=source)).count()
        pages = total / page_size + 1
        result = HanziSet.objects.filter(Q(radical=q) & Q(source=source)).values('source', 'max_strokes', 'hanzi_char',
                                                                                 'hanzi_pic_id').order_by(
            'max_strokes')[(page_num - 1) * page_size: page_num * page_size]
    else:
        strokes = radical_strokes_num + left_stroke
        print strokes
        total = HanziSet.objects.filter(Q(radical=q) & Q(source=source) & Q(max_strokes=strokes)).count()
        pages = total / page_size + 1
        result = HanziSet.objects.filter(Q(radical=q) & Q(source=source) & Q(max_strokes=strokes)).values('source',
                                                                                                          'max_strokes',
                                                                                                          'hanzi_char',
                                                                                                          'hanzi_pic_id').order_by(
            'max_strokes')[(page_num - 1) * page_size: page_num * page_size]

    a = []
    for item in result:
        item['pic_url'] = get_pic_url_by_source_pic_name(source, item['hanzi_pic_id'])
        item['remain_strokes_num'] = item['max_strokes'] - radical_strokes_num
        a.append(item)

    b = {}
    b['q'] = q
    b['total'] = total
    b['source'] = source
    b['page_num'] = page_num
    b['pages'] = pages
    b['page_size'] = page_size
    b['left_stroke'] = left_stroke
    b['result'] = a

    d = json.dumps(b, ensure_ascii=False)
    # write_log("dicts_search.txt",d)
    return HttpResponse(d, content_type="application/json")
