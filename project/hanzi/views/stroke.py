# coding=utf-8

import re
import operator
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from backend.utils import *
from backend.models import HanziParts, HanziSet


def stroke_search(request):
    """
    部件笔画检字法页面
    """
    return render(request, 'stroke_search.html', {
        'part_list': __get_parts(),
        'lqhanzi_font_path': get_lqhanzi_font_path(),
    })


def ajax_stroke_search(request):
    """
    包括一般检索，正则检索两种模式。
    1、一般检索。检索式由结构、部件序列、笔画、相似部件构成。其中，部件序列不允许出现结构符号。
    2、正则检索。检索式由IDS、笔画、相似部件构成。其中，IDS是结构、部件和正则符号的混合字符串。
    多字节汉字的正则表达式为[\u3400-\uFFFF\U00010000-\U0002FFFF\U000F0000-\U000FFFFF]。
    windows下的unicode采用的usc2，linux下采用的是usc4，多字节汉字的情况，上述正则式在windows不能工作，linux可以工作。
    """
    # 定义汉字的unicode范围
    hanzi_range = ur"\u3400-\uffff"  # for windows, temporary use
    hanzi_range = ur"\u3400-\uffff\U00010000-\U0002ffff\U000f0000-\U000fffff"  # for linux

    q = request.GET.get('q', None)
    if not q:
        return JsonResponse({"msg": "Empty input."})
    page_size = int(request.GET.get('page_size', 100))
    page_num = int(request.GET.get('page_num', 1))
    input_mode = int(request.GET.get('mode', 1))  # input_mode=1，一般检索；input_mode=2，正则检索
    output_mode = input_mode
    query_list = [Q(is_for_search=1)]

    # 提取相似部件
    pattern_similar = re.compile(ur"~[" + hanzi_range + ur"]")
    similar_parts = pattern_similar.findall(q)
    for similar_part in similar_parts:
        p = similar_part.replace('~', '')
        query_list.append(Q(stroke_serial__contains=p) | Q(similar_parts__contains=p))
        q = q.replace(similar_part, '')

    # 校验模式：如果表达式为“结构+字符+结构”或“字符+结构”，则模式应为正则检索
    pattern_mode = re.compile(ur"^[⿱⿰⿵⿶⿷󰃾⿺󰃿⿹⿸⿻⿴]?[^⿱⿰⿵⿶⿷󰃾⿺󰃿⿹⿸⿻⿴]+[⿱⿰⿵⿶⿷󰃾⿺󰃿⿹⿸⿻⿴].*")
    if pattern_mode.match(q):
        output_mode = 2

    if output_mode == 1:  # 一般检索
        pattern_normal = re.compile(ur"^([⿱⿰⿵⿶⿷󰃾⿺󰃿⿹⿸⿻⿴]?)([" + hanzi_range + ur"]*)((\d+)(-\d+)?)?$")
        m = pattern_normal.match(q)
        if m is None:
            return JsonResponse({"msg": "Invalid input, format error."})
        if m.group(1):  # 结构
            structure = m.group(1)
            query_list.append(Q(structure__contains=structure))
        if m.group(2):  # 部件序列
            s = m.group(2)
            l = list(s)
            l.sort()
            s = "".join(l)
            parts = re.sub(ur"([" + hanzi_range + ur"])", ur"\1.*", s)
            # parts = re.sub(ur"([" + hanzi_range + ur"])", ur"\1.*", m.group(2))
            query_list.append(Q(stroke_serial__regex=parts))
        if m.group(3):  # 笔画
            parts_strokes = 0
            if m.group(2):
                parts_strokes = __get_parts_strokes(m.group(2))
            start, end = __get_stroke_range(m.group(3))
            if start:
                query_list.append(Q(min_strokes__gte=parts_strokes + start))
                query_list.append(Q(max_strokes__lte=parts_strokes + end))

    elif output_mode == 2:  # 正则检索
        pattern_regex = re.compile(ur"^(([⿱⿰⿵⿶⿷󰃾⿺󰃿⿹⿸⿻⿴]|[" + hanzi_range + ur"]|[sS\(\)\[\]\^\$\*\+\.\,\?\:\=\!\|\\]|(\{[0-9\,]+\}))+)((\d+)(-\d+)?)?$")
        m = pattern_regex.match(q)
        if m is None:
            return JsonResponse({"msg": "Invalid input, format error."})
        if m.group(1):  # IDS
            ids = __format_ids(m.group(1))
            query_list.append(Q(mix_split__regex=ids))
        if m.group(4):  # 笔画
            parts_strokes = 0
            if m.group(1):
                parts = re.sub(ur"([^" + hanzi_range + ur"])", "", m.group(1))  # 提取部件
                parts_strokes = __get_parts_strokes(parts)
            start, end = __get_stroke_range(m.group(4))
            if start:
                query_list.append(Q(min_strokes__gte=parts_strokes + start))
                query_list.append(Q(max_strokes__lte=parts_strokes + end))

    total = HanziSet.objects.filter(reduce(operator.and_, query_list)).count()
    # return HttpResponse(str(HanziSet.objects.filter(reduce(operator.and_, query_list)).query))

    hanzi_set = HanziSet.objects.filter(reduce(operator.and_, query_list)).values('source', 'hanzi_char', 'hanzi_pic_id', 'seq_id', 'radical', 'max_strokes', 'std_hanzi',
                                                                                  'min_split').order_by('source')[(page_num - 1) * page_size: page_num * page_size]
    hanzi_set = list(hanzi_set)
    for item in hanzi_set:
        item['pic_url'] = get_pic_url_by_source_pic_name(item['source'], item['hanzi_pic_id'])

    return JsonResponse({
        'q': request.GET.get('q'),
        'result': hanzi_set,
        'total': total,
        'page_size': page_size,
        'page_num': page_num,
        'mode': output_mode,
    })


def inverse_search(request):
    """
    反查编码
    """
    q = request.GET.get('q', None)
    if not q:
        return JsonResponse({"msg": "Empty input."})

    hanzi_set = HanziSet.objects.filter(Q(hanzi_char__contains=q) | Q(hanzi_pic_id=q) | Q(seq_id__regex='^' + q + '(;|$)')).filter(Q(is_for_search=1)).values(
        'source', 'hanzi_char', 'hanzi_pic_id', 'std_hanzi', 'as_std_hanzi', 'mix_split', 'similar_parts', 'min_split', 'stroke_serial')
    hanzi_set = list(hanzi_set)

    if len(hanzi_set) > 0:
        ret = list(hanzi_set)[0]
        if ret['hanzi_pic_id']:
            ret['pic_url'] = get_pic_url_by_source_pic_name(ret['source'], ret['hanzi_pic_id'])
        return JsonResponse(ret)

    return JsonResponse({})


def __get_parts_strokes(parts):
    """
    从lq_hanzi_set表得到字符串中所有部件的笔画和
    """
    stroke_num = 0
    if not parts:
        return None
    for item in parts:
        part = HanziSet.objects.filter(Q(hanzi_char=item) & Q(max_strokes__isnull=False)).order_by('source')
        if len(part) > 0:
            stroke_num += part[0].max_strokes
    return stroke_num


# def __format_ids(ids):
#     """
#     格式化IDS，在连续的汉字之间加上.*以便进一步正则查询
#     """
#     # 定义汉字的unicode范围
#     hanzi_range = ur"\u3400-\uffff"  # for windows, temporary use
#     # hanzi_range = ur"\u3400-\uffff\U00010000-\U0002ffff\U000f0000-\U000fffff" # for linux

#     pattern = re.compile(ur"^[" + hanzi_range + ur"]$")
#     ret = u''
#     for i in range(len(ids) - 1):
#         ret += ids[i]
#         if pattern.match(ids[i]) and pattern.match(ids[i + 1]):  # 连续汉字
#             ret += '.*'
#     return ret + ids[len(ids) - 1]


#wxf modified
def __format_ids(ids):
    """
    格式化IDS，在连续的汉字之间加上.*以便进一步正则查询
    """
    ret = u''
    for i in range(len(ids) - 1):
        ret += ids[i]
        if ids[i] and ids[i+1]:  # 连续汉字
            ret += '.*'
    return ret + ids[len(ids) - 1]


def __get_parts():
    """
    获取部件表的部件
    """
    parts = HanziParts.objects.filter(is_search_part=1).values('part_char', 'strokes', 'stroke_order').order_by('strokes', 'stroke_order')
    res = []
    flag = 0
    for part in parts:
        if part['strokes'] != flag:
            flag = part['strokes']
            res.append({"flag": flag})
            res.append(part)
        else:
            res.append(part)
    return res


def __get_stroke_range(stroke_range):
    """
    获取笔画范围
    stroke_range的格式可以为n/n-m，输出分别对应n,n/n,m
    """
    m = re.match(ur'(\d+)(-\d+)?', stroke_range)
    if not m:
        return None

    if m.group(1):
        start = int(m.group(1))
    if m.group(2):
        end = int(m.group(2).replace('-', ''))
    else:
        end = start

    return start, end


def __write_log(filename, string):
    """
    输出调试信息到文件
    """
    fo = open(filename, "w+")
    fo.truncate()
    fo.write(string.encode('utf-8'))
    fo.close()
