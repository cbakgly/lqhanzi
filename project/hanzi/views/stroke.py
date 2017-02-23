# coding=utf-8
# hanzi/stroke.py
import json
import re
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from backend.utils import get_lqhanzi_font_path
from backend.utils import get_pic_url_by_source_pic_name
from backend.models import HanziParts, HanziSet


def write_log(filename, string):
    """
    输出调试信息到文件
    """
    fo = open(filename, "w+")
    fo.truncate()
    fo.write(string.encode('utf-8'))
    fo.close()


def get_pages(total, page_size):
    """
    得到总页数，total是数据数，page_size是每页显示的数据数
    """
    if(total % page_size == 0):
        return total / page_size
    else:
        return total / page_size + 1


def get_parts_strokes(string):
    """
    得到字符串中所有部件的笔画和
    """
    num = 0
    if string is None:
        return None
    for item in string:
        part = HanziParts.objects.filter(
            Q(part_char=item) & Q(is_search_part=1))  # .get()
        if(len(part) > 0):
            num += part[0].strokes
    return num


def remove_similar_parts(s):
    """
    #去除相似部件,s是一个字符串，可能含有结构、部件、剩余笔画范围
    """
    if s is None:
        return None
    r = ''
    length = len(s)
    for i in range(length):
        if(s[i] and s[i] != '~'):
            r += s[i]
        else:
            i += 2
    return r


def is_structure(ch):
    """
    #判断ch是不是结构字符
    """
    s = '⿰⿱⿴⿵⿶⿷󰃾⿸⿹⿺󰃿⿻'
    if(s.find(ch) != -1):
        return True
    else:
        return False


def is_regular(ch):
    """
    判断ch是不是正则表达式所用的字符
    """
    s = '(){}[]/^$*+,?.:=!|-'
    if(s.find(ch) != -1):
        return True
    else:
        return False


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
    if string is None:
        return None
    rex = '.*'
    for item in string:
        rex += item
        rex += '.*'
    return rex


def create_query_regex(string):
    """
    正则检索，解析输入，处理输入
    """
    if string is None:
        return None
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
    if string is None:
        return None
    r = ''
    length = len(string)
    for i in range(length):
        if(string[i] == '~' and string[i + 1]):
            r += string[i + 1]
    return r


def extract_structure(string):
    """
    如果首字符是结构字符，返回这个字符
    """
    if string is None:
        return None
    if(is_structure(string[0])):
        return string[0]
    else:
        return ''


def extract_parts(string):
    """
    提取部件，写入返回字等串里
    """
    if string is None:
        return None
    r = ''
    length = len(string)
    for i in range(length):
        if(i == 0 and is_structure(string[i])):
            continue
        elif (string[i].isdigit()):
            break
        else:
            r += string[i]
    return r


def get_parts():
    """
    取部件
    """
    parts = HanziParts.objects.filter(is_search_part=1)\
        .values('part_char', 'strokes', 'stroke_order')\
        .order_by('strokes', 'stroke_order')

    d = []
    flag = 0
    length = len(parts)
    for i in range(length):
        if(parts[i]['strokes'] != flag):
            flag = parts[i]['strokes']
            d.append({"flag": flag})
            d.append(parts[i])
        else:
            d.append(parts[i])
    return d


def stroke_search(request):
    """
    输出部件笔画页面
    """
    content = {}
    content['part_list'] = get_parts()
    content['lqhanzi_font_path'] = get_lqhanzi_font_path()
    return render(request, 'stroke_search.html', content)


def stroke_normal_search(request):
    """
    一般检索
    """
    q = request.GET.get('q', None)
    page_size = request.GET.get('page_size', None)
    page_num = request.GET.get('page_num', None)

    if(q is None or page_size is None or page_num is None):
        return HttpResponse("Invalid input   aaaa")

    page_size = int(page_size)
    page_num = int(page_num)

    # 检查字符串有效性，提取剩余笔画范围
    # 模式1表示末尾无数字
    # 模式2表示末尾有一个数字,
    # 模式3表示末尾两有个数字，中间有逗号
    # if
    # re.match(r'^([^\w,;:`%?&*^(){}@!|]+?)(\d+-\d+)|([^\w,;:`%?&*^(){}@!|]+?)(\d+)|([^\w,;:`%?&*^(){}@!|]+)$',q):
    m = re.match(
        r'^([^\w,;:`%?&*^(){}@!|]+?)(\d+.*)|([^\w,;:`%?&*^(){}@!|]+)$', q)
    if m:
        if(m.group(2)):
            stroke_range = m.group(2)
            if stroke_range.find('-') != -1:
                mode = 3
            else:
                mode = 2
        else:
            mode = 1
    else:
        return HttpResponse("Invalid input")

    # 提取相似部件,构建查询相似部件所用到的正则表达式
    similar_parts = extract_similar_parts(q)
    similar_parts_rex = create_regex(similar_parts)

    # 去掉相似部件,包括前边的~号
    q = remove_similar_parts(q)

    # 提取结构字符
    structure = extract_structure(q)

    # 提取部件（去掉相似部件之后的）,构建查询所有部件所用到的正则表达式
    parts = extract_parts(q)

    tmp_list = sorted(parts)
    parts = "".join(tmp_list)

    parts_rex = create_regex(parts)

    # 开始检索
    if(mode == 1):
        total = HanziSet.objects.filter(
            Q(
                structure__contains=structure) & Q(
                stroke_serial__regex=parts_rex) & Q(
                similar_parts__regex=similar_parts_rex) & Q(
                    is_for_search=1)).count()

        pages = get_pages(total, page_size)

        result = HanziSet.objects.filter(
            Q(
                structure__contains=structure) & Q(
                stroke_serial__regex=parts_rex) & Q(
                similar_parts__regex=similar_parts_rex) & Q(
                    is_for_search=1)) .values(
                        'source',
                        'hanzi_char',
                        'hanzi_pic_id',
                        'seq_id',
                        'radical',
                        'max_strokes',
                        'std_hanzi',
                        'min_split') .order_by('source')[
                            (page_num - 1) * page_size: page_num * page_size]

    elif(mode == 2):

        left_stroke = int(stroke_range)
        parts_stroke = get_parts_strokes(parts)
        strokes = parts_stroke + left_stroke

        total = HanziSet.objects.filter(
            Q(
                max_strokes=strokes) & Q(
                structure__contains=structure) & Q(
                stroke_serial__regex=parts_rex) & Q(
                    similar_parts__regex=similar_parts_rex) & Q(
                        is_for_search=1)).count()

        pages = get_pages(total, page_size)

        result = HanziSet.objects.filter(
            Q(
                max_strokes=strokes) & Q(
                structure__contains=structure) & Q(
                stroke_serial__regex=parts_rex) & Q(
                    similar_parts__regex=similar_parts_rex) & Q(
                        is_for_search=1)) .values(
                            'source',
                            'hanzi_char',
                            'hanzi_pic_id',
                            'seq_id',
                            'radical',
                            'max_strokes',
                            'std_hanzi',
                            'min_split') .order_by('source')[
                                (page_num - 1) * page_size: page_num * page_size]

    elif(mode == 3):

        parts_stroke = get_parts_strokes(parts)

        t = stroke_range.split('-')
        min_num = parts_stroke + int(t[0])
        max_num = parts_stroke + int(t[1])

        total = HanziSet.objects.filter(
            Q(
                max_strokes__lte=max_num) & Q(
                max_strokes__gte=min_num) & Q(
                structure__contains=structure) & Q(
                    stroke_serial__regex=parts_rex) & Q(
                        similar_parts__regex=similar_parts_rex) & Q(
                            is_for_search=1)).count()

        pages = get_pages(total, page_size)

        result = HanziSet.objects.filter(
            Q(
                max_strokes__lte=max_num) & Q(
                max_strokes__gte=min_num) & Q(
                structure__contains=structure) & Q(
                    stroke_serial__regex=parts_rex) & Q(
                        similar_parts__regex=similar_parts_rex) & Q(
                            is_for_search=1)) .values(
                                'source',
                                'hanzi_char',
                                'hanzi_pic_id',
                                'seq_id',
                                'radical',
                                'max_strokes',
                                'std_hanzi',
                                'min_split') .order_by('source')[
                                    (page_num - 1) * page_size: page_num * page_size]

    for item in result:
        if(item['hanzi_pic_id'] != ""):
            item['pic_url'] = get_pic_url_by_source_pic_name(
                item['source'], item['hanzi_pic_id'])

    print page_num,'/',pages
    r = {}
    r['q'] = request.GET.get('q')
    r['total'] = total
    r['page_num'] = page_num
    r['pages'] = pages
    r['page_size'] = page_size
    r['result'] = list(result)

    d = json.dumps(r, ensure_ascii=False)
    return HttpResponse(d, content_type="application/json")


def stroke_advanced_search(request):
    """
    正则检索
    """
    q = request.GET.get('q', None)
    page_size = request.GET.get('page_size', None)
    page_num = request.GET.get('page_num', None)

    if(q is None or page_size is None or page_num is None):
        return HttpResponse("Invalid input 22222")

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
    similar_parts = extract_similar_parts(q)
    similar_parts_rex = create_regex(similar_parts)

    # 去掉相似部件,包括前边的~号
    q = remove_similar_parts(q)

    # 解析结构及部件查询字符串
    query_rex = create_query_regex(parts)

    try:
        # 开始检索
        if(mode == 1):
            total = HanziSet.objects.filter(Q(mix_split__regex=query_rex) & Q(
                similar_parts__regex=similar_parts_rex) & Q(is_for_search=1)).count()

            pages = get_pages(total, page_size)

            result = HanziSet.objects.filter(
                Q(
                    mix_split__regex=query_rex) & Q(
                    similar_parts__regex=similar_parts_rex) & Q(
                    is_for_search=1)) .values(
                'source',
                'hanzi_char',
                'hanzi_pic_id',
                'seq_id',
                'radical',
                'max_strokes',
                'std_hanzi',
                'min_split') .order_by('source')[
                        (page_num - 1) * page_size: page_num * page_size]

        elif(mode == 2):

            left_stroke = int(stroke_range)
            parts_stroke = get_parts_strokes(parts)
            strokes = parts_stroke + left_stroke

            total = HanziSet.objects.filter(
                Q(
                    max_strokes=strokes) & Q(
                    mix_split__regex=query_rex) & Q(
                    similar_parts__regex=similar_parts_rex) & Q(
                    is_for_search=1)).count()

            pages = get_pages(total, page_size)

            result = HanziSet.objects.filter(
                Q(
                    max_strokes=strokes) & Q(
                    mix_split__regex=query_rex) & Q(
                    similar_parts__regex=similar_parts_rex) & Q(
                    is_for_search=1)) .values(
                        'source',
                        'hanzi_char',
                        'hanzi_pic_id',
                        'seq_id',
                        'radical',
                        'max_strokes',
                        'std_hanzi',
                        'min_split') .order_by('source')[
                            (page_num - 1) * page_size: page_num * page_size]

        elif(mode == 3):

            t = stroke_range.split('-')
            parts_stroke = get_parts_strokes(parts)
            min_num = parts_stroke + int(t[0])
            max_num = parts_stroke + int(t[1])

            total = HanziSet.objects.filter(
                Q(
                    max_strokes__lte=max_num) & Q(
                    max_strokes__gte=min_num) & Q(
                    mix_split__regex=query_rex) & Q(
                    similar_parts__regex=similar_parts_rex) & Q(
                        is_for_search=1)).count()

            pages = get_pages(total, page_size)

            result = HanziSet.objects.filter(
                Q(
                    max_strokes__lte=max_num) & Q(
                    max_strokes__gte=min_num) & Q(
                    mix_split__regex=query_rex) & Q(
                    similar_parts__regex=similar_parts_rex) & Q(
                        is_for_search=1)) .values(
                            'source',
                            'hanzi_char',
                            'hanzi_pic_id',
                            'seq_id',
                            'radical',
                            'max_strokes',
                            'std_hanzi',
                            'min_split') .order_by('source')[
                                (page_num - 1) * page_size: page_num * page_size]

    except HanziSet.OperationalError as e:
        print repr(e)

    for item in result:
        if(item['hanzi_pic_id'] != ""):
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
                is_for_search=1)) .values(
            'source',
            'hanzi_char',
            'hanzi_pic_id',
            'std_hanzi',
            'as_std_hanzi',
            'mix_split',
        )

        if(res[0]['hanzi_pic_id'] != ""):
            res[0]['pic_url'] = get_pic_url_by_source_pic_name(
                res[0]['source'], res[0]['hanzi_pic_id'])

        d = json.dumps(res[0], ensure_ascii=False)
        return HttpResponse(d, content_type="application/json")

    except BaseException as e:
        print repr(e)
        return HttpResponse("none")
