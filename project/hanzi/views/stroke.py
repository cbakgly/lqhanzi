# coding=utf-8

import json
import re
from django.core.serializers import serialize
from django.db.models import Q
# from django.forms.models import model
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response
from backend.utils import get_pic_url_by_source_pic_name
from backend.utils import get_dunhuang_dict_path
from backend.utils import get_hanyu_dict_path
from backend.models import HanziParts, HanziSet, HanziRadicals


# 构造有序查询所用的正式表达式
def create_query_regex(string):
    if string is None or len(string) == 0:
        return None

    rex = '.*'
    for item in string:
        # 如果不是结构符
        if is_structure(item) == False:
            res = HanziSet.objects.filter(Q(hanzi_char=item) & Q(source=1))
            if res[0].mix_split != '':
                rex += '<'
                rex += item
                rex += '>'
                rex += res[0].mix_split
            else:
                rex += item
            rex += '.*'
        else:
            rex += item
            rex += '.*'
    return rex


# 得到一个列表中所有部件的笔画数总和
def get_parts_strokes(parts_list):
    num = 0
    if parts_list is None or len(parts_list) == 0:
        return None
    for item in parts_list:
        part = HanziPart.objects.filter(
            Q(part_char=item) & Q(is_search_part=1))  # .get()
        if (len(part) > 0):
            num += part[0].strokes
    return num


# 去除相似部件,t是一个字符串，可能含有结构、部件、剩余笔画范围
def remove_similar_parts(s):
    if s is None or len(s) == 0:
        return None
    r = ''
    length = len(s)
    for i in range(length):
        if (s[i] and s[i] != '~'):
            r += s[i]
        else:
            i += 2
    return r


# 判断ch是不是结构类符
def is_structure(ch):
    if ch == '⿰' or ch == '⿱' or ch == '⿵' or ch == '⿶' or ch == '⿷' or ch == '󰃾' or ch == '⿺' or ch == '󰃿' or ch == '⿹' or ch == '⿸' or ch == '⿻' or ch == '⿴':
        return True
    else:
        return False


# 从一个字符串中检出所有部件来,返回一个字符串
# def get_only_parts(parts_list):

# 	if parts_list is None or len(parts_list)==0:
# 		return None

#  	r = ''
# 	for item in parts_list:
# 		if is_structure(item) == False :
# 			r += item
# 	return r


# 构造一个正式表达式
def create_regex(parts_list):
    rex = '.*'
    for item in parts_list:
        rex += item
        rex += '.*'
    return rex


# 提取相似部件，返回一个字等串
def extract_similar_parts(string):
    if string is None or len(string) == 0:
        return None
    r = ''
    length = len(string)
    for i in range(length):
        if (string[i] == '~' and string[i + 1]):
            r += string[i + 1]
    return r


# 提取结构，返回一个字符
def extract_structure(string):
    if string is None or len(string) == 0:
        return None
    if (is_structure(string[0]) == True):
        return string[0]
    else:
        return ''


# 提取部件，返回一个字等串
def extract_parts(string):
    if string is None or len(string) == 0:
        return None
    r = ''
    length = len(string)
    for i in range(length):
        if (i == 0 and is_structure(string[i]) == True):
            continue
        elif (string[i].isdigit() == True):
            break
        else:
            r += string[i]


'''
取部件函数
'''


@csrf_exempt
def get_parts():
    parts = HanziParts.objects.filter(is_search_part=1).order_by('strokes',
                                                                 'stroke_order')
    a = serialize("json", parts, ensure_ascii=False)
    b = json.loads(a)
    c = []
    for item in b:
        c.append(item['fields'])

    d = []
    flag = 0
    length = len(c)
    for i in range(length):
        if (c[i]['strokes'] != flag):
            flag = c[i]['strokes']
            d.append({"flag": flag})
            d.append(c[i])
        else:
            d.append(c[i])
    return d


'''
hanzi首页
'''


def index(request):
    return render(request, 'stroke_search.html')


'''
部件笔画页面
'''


def stroke_search(request):
    content = {}
    content['part_list'] = get_parts()
    return render(request, 'stroke_search.html', content)


def stroke_normal_search(request):
    """
    部件笔画查询函数
    """
    q = request.GET.get('q', None)
    page_size = request.GET.get('page_size', None)
    page_num = request.GET.get('page_num', None)

    if (q is None or page_size is None or page_num is None):
        return HttpResponse("Invalid input")

    # if re.search(r'^[\w,;:`%?&*^(){}@!|]+$',q) is not None:
    # 	return HttpResponse("Invalid input")

    if re.match(
            r'^[^\w,;:`%?&*^(){}@!|]+?\d+-\d+|[^\w,;:`%?&*^(){}@!|]+?\d+|[^\w,;:`%?&*^(){}@!|]+$',
            q) is None:
        return HttpResponse("Invalid input")
    else:
        print 'ok'

    page_size = int(page_size)
    page_num = int(page_num)

    WorkMode = 0  # 剩余笔画模式
    StrokeRange = ''  # 与剩余笔画有关的字符串
    structure = ''  # 结构字符
    parts_list = []  # 部件列表

    # 提取相似部件
    similar_parts = extract_similar_parts(q)

    # 去掉检索字符串的~字符
    q.replace('~', '')

    # 判断剩余笔画范围并且提取结构字符和部件序列
    # 模式1表示末尾无数字
    # 模式2表示末尾有一个数字,
    # 模式3表示末尾两有个数字，中间有逗号

    m = re.match(r'^([⿱⿰⿵⿶⿷󰃾⿺󰃿⿹⿸⿻⿴]?)([^\w,;:`%?&*^(){}@!|]+?)(\d+-\d+)$', q)
    if m:
        WorkMode = 3
        structure = m.group(1)
        parts_list.extend(m.group(2))
        parts_list.sort()
        StrokeRange = m.group(3)
        print '3'
    else:
        m = re.match(r'^([⿱⿰⿵⿶⿷󰃾⿺󰃿⿹⿸⿻⿴]?)([^\w,;:`%?&*^(){}@!|]+?)(\d+)$', q)
        if m:
            WorkMode = 2
            structure = m.group(1)
            parts_list.extend(m.group(2))
            parts_list.sort()
            StrokeRange = m.group(3)
            print '2'
        else:
            m = re.match(r'^(.{1})([^\w,;:`%?&*^(){}@!|]+)$', q)
            if m:
                WorkMode = 1
                structure = m.group(1)
                print len(structure)
                parts_list.extend(m.group(2))
                parts_list.sort()
                print len(parts_list)
                print '1'
            else:
                print 'input valid'

    # 构建查询相似部件所用到的正则表达式
    similar_parts_rex = create_regex(similar_parts)

    # 构建查询所有部件所用到的正则表达式
    parts_rex = create_regex(parts_list)

    # 开始检索
    if (WorkMode == 1):
        total = HanziSet.objects.filter(Q(structure__contains=structure) & Q(
            stroke_serial__regex=parts_rex) & Q(
            similar_parts__regex=similar_parts_rex)).count()
        pages = total / page_size + 1
        result = HanziSet.objects.filter(Q(structure__contains=structure) & Q(
            stroke_serial__regex=parts_rex) & Q(
            similar_parts__regex=similar_parts_rex)).order_by('source')[
                 (page_num - 1) * page_size: page_num * page_size]

    elif (WorkMode == 2):

        left_stroke = int(StrokeRange)
        parts_stroke = get_parts_strokes(parts_list)

        strokes = parts_stroke + left_stroke

        total = HanziSet.objects.filter(
            Q(max_strokes=strokes) & Q(structure__contains=structure) & Q(
                stroke_serial__regex=parts_rex) & Q(
                similar_parts__regex=similar_parts_rex)).count()
        pages = total / page_size + 1
        result = HanziSet.objects.filter(
            Q(max_strokes=strokes) & Q(structure__contains=structure) & Q(
                stroke_serial__regex=parts_rex) & Q(
                similar_parts__regex=similar_parts_rex)).order_by('source')[
                 (page_num - 1) * page_size: page_num * page_size]

    elif (WorkMode == 3):

        parts_stroke = get_parts_strokes(parts_list)

        t = StrokeRange.split('-')
        min_num = parts_stroke + int(t[0])
        max_num = parts_stroke + int(t[1])

        total = HanziSet.objects.filter(
            Q(max_strokes__lte=max_num) & Q(max_strokes__gte=min_num) & Q(
                structure__contains=structure) & Q(
                stroke_serial__regex=parts_rex) & Q(
                similar_parts__regex=similar_parts_rex)).count()
        pages = total / page_size + 1
        result = HanziSet.objects.filter(
            Q(max_strokes__lte=max_num) & Q(max_strokes__gte=min_num) & Q(
                structure__contains=structure) & Q(
                stroke_serial__regex=parts_rex) & Q(
                similar_parts__regex=similar_parts_rex)).order_by('source')[
                 (page_num - 1) * page_size: page_num * page_size]

    a = serialize("json", result, ensure_ascii=False)
    b = json.loads(a)
    c = []
    for item in b:
        c.append(item['fields'])
    for item in c:
        if (item['hanzi_pic_id'] != ""):
            item['pic_url'] = get_pic_url_by_source_pic_name(item['source'],
                                                             item[
                                                                 'hanzi_pic_id'])

    r = {}
    r['q'] = q
    r['total'] = total
    r['page_num'] = page_num
    r['pages'] = pages
    r['page_size'] = page_size
    r['result'] = c

    d = json.dumps(r, ensure_ascii=False)
    # write_log("no_order_search.txt",d)
    return HttpResponse(d, content_type="application/json")


'''
部件笔画查询函数
'''


def stroke_advanced_search(request):
    q = request.GET.get('q', None)
    page_size = request.GET.get('page_size', None)
    page_num = request.GET.get('page_num', None)

    # 较验参数有效性
    # 参数必须是四个
    if (q is None or page_size is None or page_num is None):
        return HttpResponse("Invalid input")

    # q不可以有字母和空格
    if re.search(r'[a-zA-Z\s]+', q) is not None:
        return HttpResponse("Invalid input")

    # q第一个字符必须是结构符
    if is_structure(q[0]) == False:
        return HttpResponse("Invalid input")

    page_size = int(page_size)
    page_num = int(page_num)

    WorkMode = 0  # 有三个可能的值:
    # 1,检索字符串末尾没有数字
    # 2,检索字符串末尾是一个数字，比如5
    # 3,检索字符串末尾是数字加逗号加数字，比如4,5
    StrokeRange = ''
    parts_list = ''
    structures_and_parts = ''  # 部件列表
    similar_parts = []  # 相似部件列表

    # 提取相似部件
    t = []
    t.extend(q)
    length = len(t)
    for i in range(length):
        if (t[i] == '~' and t[i + 1]):
            similar_parts.append(t[i + 1])

    # 去掉检索字符串中的~及后边的相似部件
    q = remove_similar_parts(q)

    # 判断剩余笔画范围并且提取结构字符和部件序列
    # 模式1表示末尾无数字
    # 模式2表示末尾有一个数字,
    # 模式3表示末尾两有个数字，中间有逗号
    m = re.match(r'^(.+?)(\d+\,\d+)$', q)
    if m:
        WorkMode = 3
        structures_and_parts = m.group(1)
        StrokeRange = m.group(2)
    else:
        m = re.match(r'^(.+?)(\d+)$', q)
        if m:
            WorkMode = 2
            structures_and_parts = m.group(1)
            StrokeRange = m.group(2)
        else:
            m = re.match(r'^(.+)$', q)
            WorkMode = 1
            structures_and_parts = m.group(1)

    # 得到部件列表
    parts_list = get_only_parts(structures_and_parts)

    # 构建查询相似部件所用到的正则表达式
    similar_parts_rex = create_regex(similar_parts)

    # 构建正则表达式
    query_rex = create_query_regex(structures_and_parts)

    # 开始检索
    if (WorkMode == 1):

        total = HanziSet.objects.filter(
            Q(mix_split__regex=query_rex) & Q(
                similar_parts__regex=similar_parts_rex)).count()
        pages = total / page_size + 1
        result = HanziSet.objects.filter(
            Q(mix_split__regex=query_rex) & Q(
                similar_parts__regex=similar_parts_rex)).order_by('source')[
                 (page_num - 1) * page_size: page_num * page_size]

    elif (WorkMode == 2):

        left_stroke = int(StrokeRange)
        parts_stroke = get_parts_strokes(parts_list)
        strokes = parts_stroke + left_stroke

        total = HanziSet.objects.filter(
            Q(max_strokes=strokes) & Q(mix_split__regex=query_rex) & Q(
                similar_parts__regex=similar_parts_rex)).count()
        pages = total / page_size + 1
        result = HanziSet.objects.filter(
            Q(max_strokes=strokes) & Q(mix_split__regex=query_rex) & Q(
                similar_parts__regex=similar_parts_rex)).order_by('source')[
                 (page_num - 1) * page_size: page_num * page_size]

    elif (WorkMode == 3):

        t = StrokeRange.split(',')
        parts_stroke = get_parts_strokes(parts_list)
        min_num = parts_stroke + int(t[0])
        max_num = parts_stroke + int(t[1])

        total = HanziSet.objects.filter(
            Q(max_strokes__lte=max_num) & Q(max_strokes__gte=min_num) & Q(
                mix_split__regex=query_rex) & Q(
                similar_parts__regex=similar_parts_rex)).count()
        pages = total / page_size + 1
        result = HanziSet.objects.filter(
            Q(max_strokes__lte=max_num) & Q(max_strokes__gte=min_num) & Q(
                mix_split__regex=query_rex) & Q(
                similar_parts__regex=similar_parts_rex)).order_by('source')[
                 (page_num - 1) * page_size: page_num * page_size]

    a = serialize("json", result, ensure_ascii=False)
    b = json.loads(a)
    c = []
    for item in b:
        c.append(item['fields'])
    for item in c:
        if (item['hanzi_pic_id'] != ""):
            item['pic_url'] = get_pic_url_by_source_pic_name(item['source'],
                                                             item[
                                                                 'hanzi_pic_id'])

    r = {}
    r['q'] = q
    r['total'] = total
    r['page_num'] = page_num
    r['pages'] = pages
    r['page_size'] = page_size
    r['result'] = c

    d = json.dumps(r, ensure_ascii=False)
    # write_log("stroke_search.txt",d)
    return HttpResponse(d, content_type="application/json")


'''
反查
'''


@csrf_exempt
def inverse_search(request):
    q = request.GET.get('q', None)
    res = HanziSet.objects.filter(Q(hanzi_char=q) & Q(source=1)).values(
        'source', 'hanzi_char', 'hanzi_pic_id',
        'std_hanzi', 'as_std_hanzi', 'mix_split', )

    if (res[0]['hanzi_pic_id'] != ""):
        res[0]['pic_url'] = get_pic_url_by_source_pic_name(res[0]['source'],
                                                           res[0][
                                                               'hanzi_pic_id'])

    d = json.dumps(res[0], ensure_ascii=False)
    return HttpResponse(d, content_type="application/json")
