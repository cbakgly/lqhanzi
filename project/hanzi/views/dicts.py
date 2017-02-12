# coding=utf-8


from django.db.models import Q
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response
from backend.utils import get_pic_url_by_source_pic_name
from backend.utils import get_dunhuang_dict_path, get_hanyu_dict_path
from backend.models import HanziParts, HanziSet, HanziRadicals
from backend.enums import SOURCE_ENUM
from tw_fuluzi import fuluzi
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
        'active': 'taiwan',
        'radical_dict': radical_dict,
        'dict_name': '台湾异体字字典',
        'welcome_url': 'https://s3.cn-north-1.amazonaws.com.cn/yitizi/index.htm',
    }

    return render(request, 'hanzi_taiwan.html', context=content)


@csrf_exempt
def taiwan_detail(request):
    """
    显示台湾异体字详细信息
    """
    seq_id = request.GET.get('seq_id', False).lower()
    if not seq_id:
        content = {'error': 'not found' + seq_id}
    else:
        base = 'https://s3.cn-north-1.amazonaws.com.cn/yitizi'
        std_code = seq_id.split('-')[0]
        anchor = False
        if len(seq_id.split('-')) > 1:
            anchor = '#bm_' + '-'.join(seq_id.split('-')[1:])
        std_type = std_code[0]
        up_url = "%s/yiti%s/w%s/w%s.htm" % (base, std_type, std_type, std_code)
        right_url = "%s/yiti%s/s%s/s%s.htm" % (base, std_type, std_type, std_code)
        if seq_id in fuluzi:
            down_url = "%s/yiti%s/fu%s/fu%s.htm" % (base, std_type, std_type, std_code)
        elif anchor:
            down_url = "%s/yiti%s/yd%s/yd%s.htm%s" % (base, std_type, std_type, std_code, anchor)
        else:
            down_url = "%s/yiti%s/%s_std/%s.htm" % (base, std_type, std_type, std_code)

        content = {
            'seq_id': seq_id.upper(),
            'up_url': up_url,
            'down_url': down_url,
            'right_url': right_url,
        }

    return render(request, 'hanzi_taiwan_detail.html', context=content)


@csrf_exempt
def taiwan_std_hanzi(request):
    """
    根据类型获取台湾异体字正字集
    """
    type = request.GET.get('type', False)
    if not type or type not in 'abcnABCN':
        return []

    page_size = int(request.GET.get('page_size', 100))  # 默认每页显示100个字
    page_num = int(request.GET.get('page_num', 1))

    query_list = [Q(source__exact=SOURCE_ENUM['taiwan']), Q(seq_id__iregex="(^|;)" + type + "[0-9]+(;|$)")]

    if request.GET.get('strokes', False):
        total_stroke = int(request.GET.get('strokes'))
        query_list.append(Q(max_strokes=total_stroke))

    total_count = HanziSet.objects.filter(reduce(operator.and_, query_list)).count()
    hanzi_set = HanziSet.objects.filter(reduce(operator.and_, query_list)).values('source', 'max_strokes', 'hanzi_char', 'hanzi_pic_id', 'seq_id').order_by(
        'max_strokes')[(page_num - 1) * page_size: page_num * page_size]
    hanzi_set = list(hanzi_set)
    for item in hanzi_set:
        item['pic_url'] = get_pic_url_by_source_pic_name(SOURCE_ENUM['taiwan'], item['hanzi_pic_id'])
        item['remain_strokes_num'] = item['max_strokes']
        item['seq_id'] = item['seq_id'].split(';')[0]

    return JsonResponse({
        'data_type': 'taiwan_std_hanzi',
        'type': type,
        'strokes': request.GET.get('strokes', ''),
        'page_size': page_size,
        'page_num': page_num,
        'total_count': total_count,
        'result': hanzi_set,
    })


@csrf_exempt
def dicts_search(request):
    """
    根据部首、来源获取相应的汉字集
    """
    if not request.GET.get('q', False) or not request.GET.get('source', False):
        return JsonResponse({'error': 'key does not exist.'})

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
    hanzi_set = HanziSet.objects.filter(reduce(operator.and_, query_list)).values('source', 'max_strokes', 'hanzi_char', 'hanzi_pic_id', 'seq_id').order_by(
        'max_strokes')[(page_num - 1) * page_size: page_num * page_size]
    hanzi_set = list(hanzi_set)

    for item in hanzi_set:
        item['pic_url'] = get_pic_url_by_source_pic_name(source, item['hanzi_pic_id'])
        item['remain_strokes_num'] = item['max_strokes'] - radical_stroke
        item['seq_id'] = item['seq_id'].split(';')[0]

    return JsonResponse({
        'data_type': 'dicts_search',
        'q': radical,
        'source': source,
        'left_stroke': request.GET.get('left_stroke', ''),
        'page_size': page_size,
        'page_num': page_num,
        'total_count': total_count,
        'result': hanzi_set,
    })


@csrf_exempt
def korean(request):
    # get radicals
    source = SOURCE_ENUM['korean']
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
        'active': 'korean',
        'radical_dict': radical_dict,
        'dict_name': '高丽异体字字典',
        'welcome_url': 'https://s3.cn-north-1.amazonaws.com.cn/yitizi/index.htm',
    }

    return render(request, 'hanzi_dicts.html', context=content)


@csrf_exempt
def hanyu(request):
    # get radicals
    source = SOURCE_ENUM['hanyu']
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
        'active': 'hanyu',
        'radical_dict': radical_dict,
        'dict_name': '高丽异体字字典',
        'welcome_url': 'https://s3.cn-north-1.amazonaws.com.cn/yitizi/index.htm',
    }

    return render(request, 'hanzi_dicts.html', context=content)


@csrf_exempt
def dunhuang(request):
    # get radicals
    source = SOURCE_ENUM['dunhuang']
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
        'active': 'dunhuang',
        'radical_dict': radical_dict,
        'dict_name': '高丽异体字字典',
        'welcome_url': 'https://s3.cn-north-1.amazonaws.com.cn/yitizi/index.htm',
    }

    return render(request, 'hanzi_dicts.html', context=content)
