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
from django.http import JsonResponse
import operator


def get_radicals(source):
    """
    根据字典来源获取部首集
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
    content = {
        'radical_dict': radical_dict,
        'dict_name': '台湾异体字字典',
        'welcome_url': 'https://s3.cn-north-1.amazonaws.com.cn/yitizi/index.htm',
    }

    return render(request, 'hanzi_dicts.html', context=content)


@csrf_exempt
def dicts_search(request):
    """
    根据部首、来源获取相应的汉字集
    """
    if not request.GET.get('q', False) or not request.GET.get('source', False):
        return []

    radical = request.GET.get('q')
    source = int(request.GET.get('source'))
    page_size = int(request.GET.get('page_size', 100))  # 默认每页显示100个字
    page_num = int(request.GET.get('page_num', 1))

    query_list = [Q(radical__exact=radical), Q(source__exact=source)]
    radical_stroke = 0
    if request.GET.get('left_stroke', False):
        total_stroke = int(request.GET.get('left_stroke'))
        try:
            radical_stroke = int(HanziRadicals.objects.get(radical=radical).strokes)
            total_stroke += radical_stroke
            query_list.append(Q(max_strokes__gte=total_stroke))
            query_list.append(Q(min_strokes__lte=total_stroke))
        except Exception:
            return []

    total_count = HanziSet.objects.filter(reduce(operator.and_, query_list)).count()
    hanzi_set = HanziSet.objects.filter(reduce(operator.and_, query_list)).values('source', 'max_strokes', 'hanzi_char', 'hanzi_pic_id').order_by(
        'max_strokes')[(page_num - 1) * page_size: page_num * page_size]
    hanzi_set = list(hanzi_set)

    for item in hanzi_set:
        item['pic_url'] = get_pic_url_by_source_pic_name(source, item['hanzi_pic_id'])
        item['remain_strokes_num'] = item['max_strokes'] - radical_stroke

    return JsonResponse({
        'q': radical,
        'source': source,
        'left_stroke': request.GET.get('left_stroke', ''),
        'page_size': page_size,
        'page_num': page_num,
        'total_count': total_count,
        'pages': total_count / page_size + 1,
        'result': hanzi_set,
    })
