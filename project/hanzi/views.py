# coding=utf-8

# hanzi/views.py
import json
import re
from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response

from backend.utils import get_pic_url_by_source_pic_name
from backend.utils import get_dunhuang_dict_path
from backend.utils import get_hanyu_dict_path
from backend.models import HanziParts, HanziSet, HanziRadicals
from appendix_hanzi import fuluzi


def write_log(filename, string):
    fo = open(filename, "w+")
    fo.truncate()
    fo.write(string.encode('utf-8'))
    fo.close()


def is_has_letter(s):
    if re.findall(r'[A-Za-z]', s):
        return True
    else:
        return False


'''
取部件函数
'''


@csrf_exempt
def get_parts():
    parts = HanziParts.objects.all().filter(is_search_part=1).order_by('strokes', 'stroke_order')
    a = serialize("json", parts, ensure_ascii=False)
    b = json.loads(a)
    c = []
    for item in b:
        c.append(item['fields'])

    # flag = 0
    # length = len(c)
    # for i in range(length):
    #   if(c[i]['strokes'] != flag):
    #       flag = c[i]['strokes']
    #       c.insert(i, {"flag":flag,"strokes":flag})
    # print len(c)
    d = []
    flag = 0
    length = len(c)
    for i in range(length):
        if(c[i]['strokes'] != flag):
            flag = c[i]['strokes']
            d.append({"flag": flag})
            d.append(c[i])
        else:
            d.append(c[i])
    return d


'''
取部首函数
'''


def get_radical():
    queryset = HanziRadicals.objects.all()
    a = serialize("json", queryset, ensure_ascii=False)
    b = json.loads(a)
    c = []
    for item in b:
        c.append(item['fields'])
    return c


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


'''
部件笔画查询函数
'''


def stroke_ajax_search(request):
    # 得到参数
    q = request.GET.get('q', None)
    order = request.GET.get('order', None)
    page_size = request.GET.get('page_size', None)
    page_num = request.GET.get('page_num', None)

    # 较验参数有效性
    # 参数必须是四个
    if(q is None or order is None or page_size is None or page_num is None):
        return HttpResponse("Invalid input")

    # q不可以有字母和空格
    if re.search(r'[a-zA-Z\s]+', q) is not None:
        return HttpResponse("Invalid input")

    # q第一个字符必须是结构符
    if not is_structure(q[0]):
        return HttpResponse("Invalid input")

    page_size = int(page_size)
    page_num = int(page_num)

    if(order == '1'):
        check_mode = 0  # 有三个可能的值:
        # 1,检索字符串末尾没有数字
        # 2,检索字符串末尾是一个数字，比如5
        # 3,检索字符串末尾是数字加逗号加数字，比如4,5
        mode_str = ''
        parts_list = ''
        structures_and_parts = ''  # 部件列表
        similar_parts = []  # 相似部件列表

        # 提取相似部件
        t = []
        t.extend(q)
        length = len(t)
        for i in range(length):
            if(t[i] == '~' and t[i+1]):
                similar_parts.append(t[i+1])

        # 去掉检索字符串中的~及后边的相似部件
        q = remove_similar_parts(q)

        # 判断剩余笔画范围并且提取结构字符和部件序列
        # 模式1表示末尾无数字
        # 模式2表示末尾有一个数字,
        # 模式3表示末尾两有个数字，中间有逗号
        m = re.match(r'^(.+?)(\d+\,\d+)$', q)
        if m:
            check_mode = 3
            structures_and_parts = m.group(1)
            mode_str = m.group(2)
        else:
            m = re.match(r'^(.+?)(\d+)$', q)
            if m:
                check_mode = 2
                structures_and_parts = m.group(1)
                mode_str = m.group(2)
            else:
                m = re.match(r'^(.+)$', q)
                check_mode = 1
                structures_and_parts = m.group(1)

        # 得到部件列表
        parts_list = get_only_parts(structures_and_parts)

        # 构建查询相似部件所用到的正则表达式
        similar_parts_rex = create_regex(similar_parts)

        # 构建正则表达式
        query_rex = create_query_regex(structures_and_parts)

        # 开始检索
        if(check_mode == 1):

            total = HanziSet.objects.filter(Q(mix_split__regex=query_rex) & Q(similar_parts__regex=similar_parts_rex)).count()
            pages = total / page_size + 1
            result = HanziSet.objects.filter(Q(mix_split__regex=query_rex) & Q(similar_parts__regex=similar_parts_rex)).order_by('source')[(page_num-1)*page_size: page_num*page_size]

        elif(check_mode == 2):

            left_stroke = int(mode_str)
            parts_stroke = get_parts_strokes(parts_list)
            strokes = parts_stroke + left_stroke

            total = HanziSet.objects.filter(Q(max_strokes=strokes) & Q(mix_split__regex=query_rex) & Q(similar_parts__regex=similar_parts_rex)).count()
            pages = total / page_size + 1
            result = HanziSet.objects.filter(Q(max_strokes=strokes) & Q(mix_split__regex=query_rex) & Q(similar_parts__regex=similar_parts_rex)).order_by('source')[(page_num-1)*page_size: page_num*page_size]

        elif(check_mode == 3):

            t = mode_str.split(',')
            parts_stroke = get_parts_strokes(parts_list)
            min_num = parts_stroke+int(t[0])
            max_num = parts_stroke+int(t[1])

            total = HanziSet.objects.filter(Q(max_strokes__lte=max_num) & Q(max_strokes__gte=min_num) & Q(mix_split__regex=query_rex) & Q(similar_parts__regex=similar_parts_rex)).count()
            pages = total / page_size + 1
            result = HanziSet.objects.filter(Q(max_strokes__lte=max_num) & Q(max_strokes__gte=min_num) & Q(mix_split__regex=query_rex) & Q(similar_parts__regex=similar_parts_rex)).order_by('source')[(page_num-1)*page_size: page_num*page_size]

        a = serialize("json", result, ensure_ascii=False)
        b = json.loads(a)
        c = []
        for item in b:
            c.append(item['fields'])
        for item in c:
            if(item['hanzi_pic_id'] != ""):
                item['pic_url'] = get_pic_url_by_source_pic_name(item['source'], item['hanzi_pic_id'])

        r = {}
        r['q'] = q
        r['order'] = order
        r['total'] = total
        r['page_num'] = page_num
        r['pages'] = pages
        r['page_size'] = page_size
        r['result'] = c

        d = json.dumps(r, ensure_ascii=False)
        # write_log("stroke_search.txt",d)
        return HttpResponse(d, content_type="application/json")

    elif(order == '2'):
        check_mode = 0  # 有三个可能的值:
        # 1,检索字符串末尾没有数字
        # 2,检索字符串末尾是一个数字，比如5
        # 3,检索字符串末尾是数字加逗号加数字，比如4,5
        mode_str = ''
        structure = ''  # 结构字符
        parts_list = []  # 部件列表
        similar_parts = []  # 相似部件列表

        # 提取相似部件
        t = []
        t.extend(q)
        length = len(t)
        for i in range(length):
            if(t[i] == '~' and t[i+1]):
                similar_parts.append(t[i+1])

        # 去掉检索字符串的~字符
        q.replace('~', '')

        # 判断剩余笔画范围并且提取结构字符和部件序列
        # 模式1表示末尾无数字
        # 模式2表示末尾有一个数字,
        # 模式3表示末尾两有个数字，中间有逗号
        m = re.match(r'^(.{1})(.+?)(\d+\,\d+)$', q)
        if m:
            check_mode = 3
            structure = m.group(1)
            parts_list.extend(m.group(2))
            parts_list.sort()
            mode_str = m.group(3)
        else:
            m = re.match(r'^(.{1})(.+?)(\d+)$', q)
            if m:
                check_mode = 2
                structure = m.group(1)
                parts_list.extend(m.group(2))
                parts_list.sort()
                mode_str = m.group(3)
            else:
                m = re.match(r'^(.{1})(.+)$', q)
                check_mode = 1
                structure = m.group(1)
                parts_list.extend(m.group(2))
                parts_list.sort()

        # 构建查询相似部件所用到的正则表达式
        similar_parts_rex = create_regex(similar_parts)

        # 构建查询所有部件所用到的正则表达式
        parts_rex = create_regex(parts_list)

        # 开始检索
        if(check_mode == 1):

            total = HanziSet.objects.filter(Q(structure__contains=structure) & Q(stroke_serial__regex=parts_rex) & Q(similar_parts__regex=similar_parts_rex)).count()
            pages = total / page_size + 1
            result = HanziSet.objects.filter(Q(structure__contains=structure) & Q(stroke_serial__regex=parts_rex) & Q(similar_parts__regex=similar_parts_rex)).order_by('source')[(page_num-1)*page_size: page_num*page_size]

        elif(check_mode == 2):

            left_stroke = int(mode_str)
            parts_stroke = get_parts_strokes(parts_list)
            strokes = parts_stroke + left_stroke

            total = HanziSet.objects.filter(Q(max_strokes=strokes) & Q(structure__contains=structure) & Q(stroke_serial__regex=parts_rex) & Q(similar_parts__regex=similar_parts_rex)).count()
            pages = total / page_size + 1
            result = HanziSet.objects.filter(Q(max_strokes=strokes) & Q(structure__contains=structure) & Q(stroke_serial__regex=parts_rex) & Q(similar_parts__regex=similar_parts_rex)).order_by('source')[(page_num-1)*page_size: page_num*page_size]

        elif(check_mode == 3):

            t = mode_str.split(',')
            parts_stroke = get_parts_strokes(parts_list)
            min_num = parts_stroke+int(t[0])
            max_num = parts_stroke+int(t[1])

            total = HanziSet.objects.filter(Q(max_strokes__lte=max_num) & Q(max_strokes__gte=min_num) & Q(structure__contains=structure) & Q(stroke_serial__regex=parts_rex) & Q(similar_parts__regex=similar_parts_rex)).count()
            pages = total / page_size + 1
            result = HanziSet.objects.filter(Q(max_strokes__lte=max_num) & Q(max_strokes__gte=min_num) & Q(structure__contains=structure) & Q(
                stroke_serial__regex=parts_rex) & Q(similar_parts__regex=similar_parts_rex)).order_by('source')[(page_num-1)*page_size: page_num*page_size]

        a = serialize("json", result, ensure_ascii=False)
        b = json.loads(a)
        c = []
        for item in b:
            c.append(item['fields'])
        for item in c:
            if(item['hanzi_pic_id'] != ""):
                item['pic_url'] = get_pic_url_by_source_pic_name(item['source'], item['hanzi_pic_id'])

        r = {}
        r['q'] = q
        r['order'] = order
        r['total'] = total
        r['page_num'] = page_num
        r['pages'] = pages
        r['page_size'] = page_size
        r['result'] = c

        d = json.dumps(r, ensure_ascii=False)
        # write_log("no_order_search.txt",d)
        return HttpResponse(d, content_type="application/json")


# 判断ch是不是结构类符
def is_structure(ch):
    if ch == '⿰' or ch == '⿱' or ch == '⿵' or ch == '⿶' or ch == '⿷' or ch == '󰃾' or ch == '⿺' or ch == '󰃿' or ch == '⿹' or ch == '⿸' or ch == '⿻' or ch == '⿴':
        return True
    else:
        return False


# 从一个字符串中检出所有部件来,返回一个字符串
def get_only_parts(parts_list):

    if parts_list is None or len(parts_list) == 0:
        return None

    r = ''
    for item in parts_list:
        if not is_structure(item):
            r += item
    return r


# 构造一个正式表达式
def create_regex(parts_list):
    rex = '.*'
    for item in parts_list:
        rex += item
        rex += '.*'
    return rex


# 构造有序查询所用的正式表达式
def create_query_regex(string):

    if string is None or len(string) == 0:
        return None

    rex = '.*'
    for item in string:
        # 如果不是结构符
        if not is_structure(item):
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
        part = HanziParts.objects.get(part_char=item)
        num += part.strokes
    return num


# 去除相似部件,t是一个字符串，可能含有结构、部件、剩余笔画范围
def remove_similar_parts(s):
    if s is None or len(s) == 0:
        return None
    r = ''
    length = len(s)
    for i in range(length):
        if(s[i] and s[i] != '~'):
            r += s[i]
        else:
            i += 2
    return r


'''
反查
'''


@csrf_exempt
def inverse_search(request):

    q = request.GET.get('q', None)
    res = HanziSet.objects.filter(Q(hanzi_char=q) & Q(source=1)).values('source', 'hanzi_char', 'hanzi_pic_id', 'std_hanzi', 'as_std_hanzi', 'mix_split',)

    if(res[0]['hanzi_pic_id'] != ""):
        res[0]['pic_url'] = get_pic_url_by_source_pic_name(res[0]['source'], res[0]['hanzi_pic_id'])

    d = json.dumps(res[0], ensure_ascii=False)
    return HttpResponse(d, content_type="application/json")


'''
异体字查询函数
'''


@csrf_exempt
def variant_search(request):
    # 得到参数
    q = request.GET.get('q', None)

    # 较验参数有效性
    # 如果缺少参数q就输出页面本身
    if(q is None):
        return render(request, 'variant_search.html')

    # 做检索操作
    result = HanziSet.objects.filter(Q(hanzi_char__contains=q) | Q(hanzi_pic_id=q)).order_by('source')
    ret = []
    for item in result:
        # 对于台湾异体字
        if(item.source == 2):
            d = {}
            d['source'] = 2
            d['content'] = []

            '''
            #获得std_hanzi字段中的所有正字和这些正字包含的异体字
            '''
            std_hanzi = item.std_hanzi.split(';')
            for item in std_hanzi:
                d1 = {}
                d1["stdchar"] = item
                if(is_has_letter(item)):
                    d1["type"] = 'pic'
                    d1["pic_url"] = get_pic_url_by_source_pic_name(2, item)
                else:
                    d1["type"] = 'char'
                d1["variant"] = []
                # 获得该类型正字的所有异体字
                result = HanziSet.objects.filter(Q(std_hanzi__contains=item) & Q(source=2)).exclude(variant_type=0)
                for item in result:
                    d2 = {}
                    if(item.hanzi_char != ''):
                        d2["type"] = "char"
                        d2["text"] = item.hanzi_char
                    else:
                        d2["type"] = "pic"
                        d2["text"] = item.hanzi_pic_id
                        d2["pic_url"] = get_pic_url_by_source_pic_name(2, item.hanzi_pic_id)

                    d1["variant"].append(d2)

                d['content'].append(d1)

            '''
            #处理兼正字的情况
            '''
            if(item.as_std_hanzi != '' and item.as_std_hanzi[0] != '#'):
                d1 = {}
                if(item.hanzi_char != ''):
                    d1["stdchar"] = item.hanzi_char
                    d1["type"] = 'char'
                elif(item.hanzi_pic_id != ''):
                    d1["stdchar"] = item.hanzi_pic_id
                    d1["type"] = 'pic'
                    d1["pic_url"] = get_pic_url_by_source_pic_name(2, item.hanzi_pic_id)

                d1["variant"] = []
                # 获得该类型正字的所有异体字
                result = HanziSet.objects.filter(Q(std_hanzi__contains=d1["stdchar"]) & Q(source=2)).exclude(variant_type=0)
                for item in result:
                    d2 = {}
                    if(item.hanzi_char != ''):
                        d2["type"] = "char"
                        d2["text"] = item.hanzi_char
                    else:
                        d2["type"] = "pic"
                        d2["text"] = item.hanzi_pic_id
                        d2["pic_url"] = get_pic_url_by_source_pic_name(2, item.hanzi_pic_id)

                    d1["variant"].append(d2)

                d['content'].append(d1)

            ret.append(d)

        # 对于汉语大字典
        elif(item.source == 3):
            # d = {}
            # d['source'] = 3
            # d['content'] = item.seq_id
            # d['pic_url'] = get_pic_url_by_source_pic_name(3,item.seq_id)
            # ret.append(d)

            d2 = {}
            if(item.hanzi_char != ''):
                d2["type"] = "char"
                d2["text"] = item.hanzi_char
            else:
                d2["type"] = "pic"
                d2["text"] = item.hanzi_pic_id
                d2["pic_url"] = get_pic_url_by_source_pic_name(2, item.hanzi_pic_id)

            # 先检测ret中有没有汉语大字典信息，如果有就直接添加，如果没有要建立新的对象
            flag = False
            for item2 in ret:
                if item2['source'] == 3:
                    flag = True
                    break

            if not flag:
                d = {}
                d['source'] = 3
                d['content'] = []
                d['content'].append(d2)
                ret.append(d)
            else:
                item2['content'].append(d2)

        # 对于高丽异体字
        elif(item.source == 4):

            # 如果ret里已经包含了高丽异体字信息，就返回
            flag = False
            for item2 in ret:
                if item2['source'] == 4:
                    flag = True
                    break
            if flag:
                continue

            # 如果ret里没有包含了高丽异体字信息，就继续
            d = {}
            d['source'] = 4
            d['content'] = []

            '''
            #获得std_hanzi字段中的所有正字和这些正字包含的异体字
            '''
            std_hanzi = item.std_hanzi.split(';')
            for item in std_hanzi:
                d1 = {}
                d1["stdchar"] = item
                if(is_has_letter(item)):
                    d1["type"] = 'pic'
                    d1["pic_url"] = get_pic_url_by_source_pic_name(4, item)
                else:
                    d1["type"] = 'char'
                d1["variant"] = []
                # 获得该类型正字的所有异体字
                result = HanziSet.objects.filter(Q(std_hanzi__contains=item) & Q(source=4)).exclude(variant_type=0)
                for item in result:
                    d2 = {}
                    if(item.hanzi_char != ''):
                        d2["type"] = "char"
                        d2["text"] = item.hanzi_char
                    else:
                        d2["type"] = "pic"
                        d2["text"] = item.hanzi_pic_id
                        d2["pic_url"] = get_pic_url_by_source_pic_name(4, item.hanzi_pic_id)

                    d1["variant"].append(d2)

                d['content'].append(d1)

            '''
            #处理兼正字的情况
            '''
            if(item.as_std_hanzi != '' and item.as_std_hanzi[0] != '#'):
                d1 = {}
                if(item.hanzi_char != ''):
                    d1["stdchar"] = item.hanzi_char
                    d1["type"] = 'char'
                elif(item.hanzi_pic_id != ''):
                    d1["stdchar"] = item.hanzi_pic_id
                    d1["type"] = 'pic'
                    d1["pic_url"] = get_pic_url_by_source_pic_name(4, item.hanzi_pic_id)

                d1["variant"] = []
                # 获得该类型正字的所有异体字
                result = HanziSet.objects.filter(Q(std_hanzi__contains=d1["stdchar"]) & Q(source=4)).exclude(variant_type=0)
                for item in result:
                    d2 = {}
                    if(item.hanzi_char != ''):
                        d2["type"] = "char"
                        d2["text"] = item.hanzi_char
                    else:
                        d2["type"] = "pic"
                        d2["text"] = item.hanzi_pic_id
                        d2["pic_url"] = get_pic_url_by_source_pic_name(4, item.hanzi_pic_id)

                    d1["variant"].append(d2)

                d['content'].append(d1)

            ret.append(d)

        elif(item.source == 5):

            d2 = {}
            if(item.hanzi_char != ''):
                d2["type"] = "char"
                d2["text"] = item.hanzi_char
            else:
                d2["type"] = "pic"
                d2["text"] = item.hanzi_pic_id
                d2["pic_url"] = get_pic_url_by_source_pic_name(2, item.hanzi_pic_id)

            # 先检测ret中有没有敦煌俗字典信息，如果有就直接添加，如果没有要建立新的对象
            flag = False
            for item2 in ret:
                if item2['source'] == 5:
                    flag = True
                    break

            if not flag:
                d = {}
                d['source'] = 5
                d['content'] = []
                d['content'].append(d2)
                ret.append(d)
            else:
                item2['content'].append(d2)

            # d['content'] = item.seq_id
            # d['pic_url'] = get_pic_url_by_source_pic_name(5,item.seq_id)

    r = json.dumps(ret, ensure_ascii=False)
    # write_log("variant_search.txt",r)
    return HttpResponse(r, content_type="application/json")


# 输入参数为list，返回值也是list
# 输入参数必须是A00111-001 或者A00111这样的字符串
def get_tw_page(code_list):
    tmp_list = []
    for item in code_list:
        if(item.find('-') != -1):
            tmp_list.append(item.split('-')[0])
        else:
            tmp_list.append(item)
    return tmp_list


def get_tw_iframe_up(code_list):

    tmp_list = []
    for item in code_list:
        # 如果不是附录字
        if fuluzi.count(item) == 0:

            # 构造模板路径
            item = item.lower()
            first_letter = item[0].lower()
            up = '/hanzi/yitizi/yiti' + first_letter + '/w' + first_letter + '/w' + item + '.htm'
            tmp_list.append(up)

        else:
            item = item.lower()
            first_letter = item[0].lower()
            up = '/hanzi/yitizi/yiti' + first_letter + '/w' + first_letter + '/w' + item + '.htm'
            tmp_list.append(up)

    return tmp_list


def get_tw_iframe_left(code_list):
    tmp_list = []
    for item in code_list:
        # 如果不是附录字
        if fuluzi.count(item) == 0:

            # 构造模板路径
            item = item.lower()
            first_letter = item[0].lower()
            left = '/hanzi/yitizi/yiti' + first_letter + '/' + first_letter + '_std/' + item + '.htm'
            tmp_list.append(left)

        else:
            item = item.lower()
            first_letter = item[0].lower()
            left = '/hanzi/yitizi/yiti' + first_letter + '/' + first_letter + '_std/' + item + '.htm'
            tmp_list.append(left)

    return tmp_list


def get_tw_iframe_right(code_list):
    tmp_list = []
    for item in code_list:
        # 如果不是附录字
        if fuluzi.count(item) == 0:

            # 构造模板路径
            item = item.lower()
            first_letter = item[0].lower()
            right = '/hanzi/yitizi/yiti' + first_letter + '/s' + first_letter + '/s' + item + '.htm'
            tmp_list.append(right)

        else:
            item = item.lower()
            first_letter = item[0].lower()
            right = '/hanzi/yitizi/yiti' + first_letter + '/s' + first_letter + '/s' + item + '.htm'
            tmp_list.append(right)

    return tmp_list


# 输入参数为list，返回值也是list
def get_tw_url(code_list):
    tmp_list = []
    for item in code_list:

        # 如果不是附录字
        if fuluzi.count(item) == 0:
            first_letter = item[0].lower()
            url = 'http://dict.variants.moe.edu.tw/yiti' + first_letter + '/fr' + first_letter + '/fr' + item + '.htm'
        else:
            first_letter = item[0].lower()
            url = 'http://dict.variants.moe.edu.tw/yiti' + first_letter + '/ur' + first_letter + '/ur' + item + '.htm'
        tmp_list.append(url)
    return tmp_list


def get_gl_url(char):
    return 'http://kb.sutra.re.kr/ritk_eng/etc/chinese/chineseBitSearch.do'


def get_hy_page(text):
    return text.split('-')[0]


@csrf_exempt
def show_yitizi(request):
    path = request.path.encode("utf-8")
    addr = path[7:len(path)]
    return render_to_response(addr)


@csrf_exempt
def variant_detail(request):
    source = request.GET['source']  # char or pic
    kind = request.GET['type']  # char or pic
    text = request.GET['text']  # 可能是文字，也可能是图片字的文件名

    TW = {}  # 如果属于台湾异体字，其编码存入数组TW_char_addr
    HY = {}  # 如果属于汉语大字典，其页码存入变量HY
    GL = {}  # 如果属于高丽异体字，则找出对应正字的所有异体字，存入glyitizi
    DH = {}  # 如果属于敦煌俗字典，其页码存入变量DH_char_page、

    result = HanziSet.objects.filter(Q(hanzi_char__contains=text) | Q(hanzi_pic_id__exact=text)).order_by('source')
    # 得到台湾字的信息
    for item in result:
        if(item.source == 2):
            if (item.variant_type == 0):  # 如果是正字

                TW['dict'] = "台湾异体字"
                TW['type'] = "正字"
                tmp_list = []
                tmp_list.append(item.seq_id)
                TW['addr'] = tmp_list
                TW['page'] = get_tw_page(TW['addr'])
                TW['url'] = get_tw_url(TW['page'])

                TW['up'] = get_tw_iframe_up(TW['page'])
                TW['left'] = get_tw_iframe_left(TW['page'])
                TW['right'] = get_tw_iframe_right(TW['page'])

                TW['a'] = zip(TW['addr'], TW['url'])
                TW['tab'] = zip(TW['addr'], TW['up'], TW['left'], TW['right'])

                TW['zhengzhi'] = item.std_hanzi
                continue

            elif (item.variant_type == 1):  # 如果是狭义异体字

                TW['dict'] = "台湾异体字"
                TW['type'] = "狭义异体字"
                tmp_list = []
                tmp_list.append(item.seq_id)
                TW['addr'] = tmp_list
                TW['page'] = get_tw_page(TW['addr'])
                TW['url'] = get_tw_url(TW['page'])

                TW['up'] = get_tw_iframe_up(TW['page'])
                TW['left'] = get_tw_iframe_left(TW['page'])
                TW['right'] = get_tw_iframe_right(TW['page'])

                TW['a'] = zip(TW['addr'], TW['url'])
                TW['tab'] = zip(TW['addr'], TW['up'], TW['left'], TW['right'])

                TW['zhengzhi'] = item.std_hanzi
                continue

            elif (item.variant_type == 2):  # 如果是异体字兼正字

                TW['dict'] = "台湾异体字"
                TW['type'] = "异体字兼正字"
                TW['addr'] = item.seq_id.split(';')
                TW['addr'].append(item.as_std_hanzi)
                TW['page'] = get_tw_page(TW['addr'])
                TW['url'] = get_tw_url(TW['page'])

                TW['up'] = get_tw_iframe_up(TW['page'])
                TW['left'] = get_tw_iframe_left(TW['page'])
                TW['right'] = get_tw_iframe_right(TW['page'])

                TW['a'] = zip(TW['addr'], TW['url'])
                TW['tab'] = zip(TW['addr'], TW['up'], TW['left'], TW['right'])

                TW['zhengzhi'] = item.std_hanzi + ';' + item.hanzi_char
                continue

            elif (item.variant_type == 3):  # 如果是广义异体字

                TW['dict'] = "台湾异体字"
                TW['type'] = "广义异体字"
                TW['addr'] = item.seq_id.split(';')
                TW['page'] = get_tw_page(TW['addr'])
                TW['url'] = get_tw_url(TW['page'])

                TW['up'] = get_tw_iframe_up(TW['page'])
                TW['left'] = get_tw_iframe_left(TW['page'])
                TW['right'] = get_tw_iframe_right(TW['page'])

                TW['a'] = zip(TW['addr'], TW['url'])
                TW['tab'] = zip(TW['addr'], TW['up'], TW['left'], TW['right'])

                TW['zhengzhi'] = item.std_hanzi
                continue

            elif (item.variant_type == 4):
                continue

        # 得到汉语大字典中的信息。处理起来比较简单。得到页码即可。
        elif(item.source == 3):
            HY['dict'] = "汉语大字典"
            HY['type'] = "正字"
            HY['addr'] = item.seq_id
            HY['page'] = ''
            if(len(get_hy_page(item.seq_id)) == 3):
                HY['page'] = get_hanyu_dict_path() + '0' + get_hy_page(item.seq_id)+'.png'
                print HY['page']
            elif(len(get_hy_page(item.seq_id)) == 4):
                HY['page'] = get_hanyu_dict_path() + get_hy_page(item.seq_id)+'.png'
                print HY['page']
            HY['zhengzhi'] = item.hanzi_char
            continue

        # 得到高丽异体字的信息。首先得到正字，再根据正字得到对应的异体字。
        # 对char型的高丽字来说，他本身就是正字
        elif(item.source == 4):
            # 如果已经有记录了，就返回，以免信息多余
            # if len(GL)>0:
            #   continue
            obj = HanziSet.objects.filter(Q(source=4) & (Q(hanzi_char__contains=text) | Q(hanzi_pic_id__exact=text))).first()
            result = HanziSet.objects.filter(Q(source=4) & Q(std_hanzi=obj.std_hanzi)).exclude(hanzi_pic_id='')
            vraiant = []
            for item in result:
                t = {}
                t['pic_id'] = item.hanzi_pic_id
                t['pic_url'] = get_pic_url_by_source_pic_name(4, item.hanzi_pic_id)
                vraiant.append(t)

            GL['dict'] = "高丽异体字"
            if (obj.variant_type == 0):  # 如果是正字
                GL['type'] = "正字"
            elif(obj.variant_type == 1):
                GL['type'] = "狭义异体字"
            GL['url'] = get_gl_url(text)
            GL['zhengzhi'] = obj.std_hanzi
            GL['vraiant'] = vraiant
            continue

        # 得到敦煌俗字典中的信息。处理起来比较简单。得到页码即可。
        elif(item.source == 5):
            DH['dict'] = "敦煌俗字典"
            DH['type'] = "正字"
            DH['addr'] = item.seq_id
            DH['page'] = get_dunhuang_dict_path()+item.seq_id+'.png'
            DH['zhengzhi'] = item.hanzi_char
            continue

    context = {}
    context['source'] = source
    context['type'] = kind
    context['text'] = text
    if(kind == 'pic'):
        context['pic_url'] = get_pic_url_by_source_pic_name(int(source), text)

    context['TW'] = TW
    context['HY'] = HY
    context['GL'] = GL
    context['DH'] = DH
    return render(request, 'hanzi_detail.html', context)


@csrf_exempt
def dicts(request):
    content = {}
    content['radical_list'] = get_radical()
    return render(request, 'hanzi_dicts.html', content)


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

    radical_strokes_num = HanziRadicals.objects.get(radical=q).strokes  # 部首笔画数

    if(left_stroke == -1):
        total = HanziSet.objects.filter(Q(radical=q) & Q(source=source)).count()
        pages = total / page_size + 1
        result = HanziSet.objects.filter(Q(radical=q) & Q(source=source)).values('source', 'max_strokes', 'hanzi_char', 'hanzi_pic_id').order_by('max_strokes')[(page_num-1)*page_size: page_num*page_size]
    else:
        strokes = radical_strokes_num + left_stroke
        print strokes
        total = HanziSet.objects.filter(Q(radical=q) & Q(source=source) & Q(max_strokes=strokes)).count()
        pages = total / page_size + 1
        result = HanziSet.objects.filter(Q(radical=q) & Q(source=source) & Q(max_strokes=strokes)).values('source', 'max_strokes', 'hanzi_char', 'hanzi_pic_id').order_by('max_strokes')[(page_num-1)*page_size: page_num*page_size]

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
