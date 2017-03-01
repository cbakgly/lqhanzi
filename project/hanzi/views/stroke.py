# coding=utf-8
import json
import re
import operator
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from backend.utils import *
from backend.models import HanziParts, HanziSet


def __write_log(filename, string):
    """
    输出调试信息到文件
    """
    fo = open(filename, "w+")
    fo.truncate()
    fo.write(string.encode('utf-8'))
    fo.close()


def __get_pages(total, page_size):
    """
    得到总页数，total是总数据条数，page_size是每页显示的数据数
    """
    if (total % page_size == 0):
        return total / page_size
    else:
        return total / page_size + 1


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


def remove_similar_parts(s):
    """
    #去除相似部件,s是一个字符串，可能含有结构、部件、剩余笔画范围
    """
    r = ''
    length = len(s)
    for i in range(length):
        if (s[i] and s[i] != '~'):
            r += s[i]
        else:
            i += 2
    return r


def is_structure(ch):
    """
    #判断ch是不是结构字符
    """
    return ch in u'⿰⿱⿴⿵⿶⿷󰃾⿸⿹⿺󰃿⿻'


def is_regular(ch):
    """
    判断ch是不是正则表达式所用的字符
    """
    return ch in '(){}[]/^$*+,?.:=!|-'


def is_part(char):
    """
    判断一个字符是不是部件
    """
    if is_structure(char) or is_regular(char):
        return False
    else:
        return True


def create_regex(string):
    """
    构造一个简单的正式表达式
    """
    rex = '.*'
    for item in string:
        rex += item
        rex += '.*'
    return rex


def create_query_regex(string):
    """
    正则检索，解析输入，处理输入
    """
    ret = ''
    length = len(string)
    for i in range(length):
        if i == length - 1:
            ret += string[i]
            return ret

        first = string[i]
        second = string[i + 1]
        if is_part(first) and is_part(second):
            ret += first
            ret += '.*'
        else:
            ret += first
    return ret


def extract_similar_parts(string):
    """
    提取相似部件，存放返回字等串里
    """
    r = ''
    length = len(string)
    for i in range(length):
        if (string[i] == '~' and string[i + 1]):
            r += string[i + 1]
    return r


def extract_structure(string):
    """
    如果首字符是结构字符，返回这个字符
    """
    if (is_structure(string[0])):
        return string[0]
    else:
        return ''


def extract_parts(string):
    """
    提取部件，写入返回字等串里
    """
    r = ''
    length = len(string)
    for i in range(length):
        if (i == 0 and is_structure(string[i])):
            continue
        elif (string[i].isdigit()):
            break
        else:
            r += string[i]
    return r


def __get_parts():
    """
    取部件
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


def stroke_search(request):
    """
    部件笔画检字法页面
    """
    return render(request, 'stroke_search.html', {
        'part_list': __get_parts(),
        'lqhanzi_font_path': get_lqhanzi_font_path(),
    })


def stroke_normal_search(request):
    """
    一般检索。
    包括结构、部件序列、笔画、相似部件等几大要素，分别提取构造检索查询条件。
    # 多字节汉字的正则表达式为[\u3400-\uFFFF\U00010000-\U0002FFFF\U000F0000-\U000FFFFF]
    """
    q = request.GET.get('q', None)
    if not q:
        return JsonResponse({"msg": "Empty input."})
    page_size = int(request.GET.get('page_size', 100))
    page_num = int(request.GET.get('page_num', 1))
    query_list = [Q(is_for_search=1)]

    # 提取相似部件。windows下的unicode采用的usc2，linux下采用的是usc4，多字节汉字的情况，这段代码在windows不能工作，linux可以工作
    # similar_parts = re.findall(u"~[\u3400-\uffff\U00010000-\U0002ffff\U000f0000-\U000fffff]", q)
    similar_parts = re.findall(u"~[\u3400-\uffff]", q)
    for similar_part in similar_parts:
        p = similar_part.replace('~', '')
        query_list.append(Q(stroke_serial__contains=p) | Q(similar_parts__contains=p))
        q = q.replace(similar_part, '')

    # 校验检索字符串的有效性
    m = re.match(ur'^([⿱⿰⿵⿶⿷󰃾⿺󰃿⿹⿸⿻⿴]?)([\u3400-\uffff]*)((\d+)(-\d+)?)?$', q)
    if m is None:
        return JsonResponse({"msg": "Invalid input."})

    if m.group(1):
        structure = m.group(1)
        query_list.append(Q(structure__contains=structure))

    if m.group(2):
        parts = re.sub(u"([\u3400-\uffff])", r"\1.*", m.group(2))
        query_list.append(Q(stroke_serial__regex=parts))

    if m.group(3):
        parts_strokes = 0
        if m.group(2):
            parts_strokes = __get_parts_strokes(m.group(2))
        strokes_begin = parts_strokes + int(m.group(4))
        query_list.append(Q(min_strokes__gte=strokes_begin))
        if m.group(5):
            strokes_end = parts_strokes + int(m.group(5).replace('-', ''))
        else:
            strokes_end = parts_strokes + int(m.group(4))
        query_list.append(Q(max_strokes__lte=strokes_end))

    total_count = HanziSet.objects.filter(reduce(operator.and_, query_list)).count()
    hanzi_set = HanziSet.objects.filter(reduce(operator.and_, query_list)).values('source', 'hanzi_char', 'hanzi_pic_id', 'seq_id', 'radical', 'max_strokes', 'std_hanzi',
                                                                                  'min_split').order_by('source')[(page_num - 1) * page_size: page_num * page_size]
    hanzi_set = list(hanzi_set)
    for item in hanzi_set:
        item['pic_url'] = get_pic_url_by_source_pic_name(item['source'], item['hanzi_pic_id'])

    return JsonResponse({
        'q': request.GET.get('q'),
        'result': hanzi_set,
        'total_count': total_count,
        'page_size': page_size,
        'page_num': page_num,
    })


def stroke_advanced_search(request):
    """
    正则检索
    """
    # print 'stroke_advanced_search'

    q = request.GET.get('q', None)
    page_size = request.GET.get('page_size', None)
    page_num = request.GET.get('page_num', None)

    if (q is None or page_size is None or page_num is None):
        return HttpResponse("Invalid input")

    page_size = int(page_size)
    page_num = int(page_num)

    # 一边检查字符串有效性，一边提取剩余笔画范围
    # 模式1表示末尾无数字
    # 模式2表示末尾有一个数字,
    # 模式3表示末尾两有个数字，中间有逗号
    m = re.match(r'^(\S+?)(\d+-\d+)$', q)
    if m:
        parts = m.group(1)
        stroke_range = m.group(2)
        mode = 3
    else:
        m = re.match(r'^(\S+?)(\d+)$', q)
        if m:
            parts = m.group(1)
            stroke_range = m.group(2)
            mode = 2
        else:
            parts = q
            mode = 1

    # 提取相似部件,构建查询相似部件所用到的正则表达式
    similar_parts = extract_similar_parts(parts)
    similar_parts_rex = create_regex(similar_parts)

    # 去掉相似部件,包括前边的~号
    parts = remove_similar_parts(parts)

    # 解析结构及部件查询字符串
    query_rex = create_query_regex(parts)

    try:
        # 开始检索
        if (mode == 1):
            total = HanziSet.objects.filter(Q(mix_split__regex=query_rex) & Q(
                similar_parts__regex=similar_parts_rex) & Q(is_for_search=1)).count()

            pages = __get_pages(total, page_size)

            result = HanziSet.objects.filter(
                Q(
                    mix_split__regex=query_rex) & Q(
                    similar_parts__regex=similar_parts_rex) & Q(
                    is_for_search=1)).values(
                'source',
                'hanzi_char',
                'hanzi_pic_id',
                'seq_id',
                'radical',
                'max_strokes',
                'std_hanzi',
                'min_split').order_by('source')[
                     (page_num - 1) * page_size: page_num * page_size]

        elif (mode == 2):

            left_stroke = int(stroke_range)
            parts_stroke = __get_parts_strokes(parts)
            strokes = parts_stroke + left_stroke

            total = HanziSet.objects.filter(
                Q(
                    max_strokes=strokes) & Q(
                    mix_split__regex=query_rex) & Q(
                    similar_parts__regex=similar_parts_rex) & Q(
                    is_for_search=1)).count()

            pages = __get_pages(total, page_size)

            result = HanziSet.objects.filter(
                Q(
                    max_strokes=strokes) & Q(
                    mix_split__regex=query_rex) & Q(
                    similar_parts__regex=similar_parts_rex) & Q(
                    is_for_search=1)).values(
                'source',
                'hanzi_char',
                'hanzi_pic_id',
                'seq_id',
                'radical',
                'max_strokes',
                'std_hanzi',
                'min_split').order_by('source')[
                     (page_num - 1) * page_size: page_num * page_size]

        elif (mode == 3):

            t = stroke_range.split('-')
            parts_stroke = __get_parts_strokes(parts)
            min_num = parts_stroke + int(t[0])
            max_num = parts_stroke + int(t[1])

            total = HanziSet.objects.filter(
                Q(
                    max_strokes__lte=max_num) & Q(
                    max_strokes__gte=min_num) & Q(
                    mix_split__regex=query_rex) & Q(
                    similar_parts__regex=similar_parts_rex) & Q(
                    is_for_search=1)).count()

            pages = __get_pages(total, page_size)

            result = HanziSet.objects.filter(
                Q(
                    max_strokes__lte=max_num) & Q(
                    max_strokes__gte=min_num) & Q(
                    mix_split__regex=query_rex) & Q(
                    similar_parts__regex=similar_parts_rex) & Q(
                    is_for_search=1)).values(
                'source',
                'hanzi_char',
                'hanzi_pic_id',
                'seq_id',
                'radical',
                'max_strokes',
                'std_hanzi',
                'min_split').order_by('source')[
                     (page_num - 1) * page_size: page_num * page_size]

    except HanziSet.OperationalError as e:
        print repr(e)

    for item in result:
        if (item['hanzi_pic_id'] != ""):
            item['pic_url'] = get_pic_url_by_source_pic_name(
                item['source'], item['hanzi_pic_id'])

    r = {}
    r['q'] = q
    r['total'] = total
    r['page_num'] = page_num
    r['pages'] = pages
    r['page_size'] = page_size
    r['result'] = list(result)

    d = json.dumps(r, ensure_ascii=False)
    return HttpResponse(d, content_type="application/json")


def inverse_search(request):
    """
    反查
    """
    try:
        q = request.GET.get('q', None)
        res = HanziSet.objects.filter(
            Q(
                hanzi_char=q) | Q(
                hanzi_pic_id=q)).filter(
            Q(
                source=1) & Q(
                is_for_search=1)).values(
            'source',
            'hanzi_char',
            'hanzi_pic_id',
            'std_hanzi',
            'as_std_hanzi',
            'mix_split',
        )

        if (res[0]['hanzi_pic_id'] != ""):
            res[0]['pic_url'] = get_pic_url_by_source_pic_name(
                res[0]['source'], res[0]['hanzi_pic_id'])

        d = json.dumps(res[0], ensure_ascii=False)
        return HttpResponse(d, content_type="application/json")

    except BaseException as e:
        print repr(e)
        return HttpResponse("none")
