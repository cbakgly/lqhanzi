# coding=utf-8
from __future__ import unicode_literals
import json
import re
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from backend.utils import get_pic_url_by_source_pic_name
from backend.utils import get_hanyu_dict_path
from backend.utils import get_dunhuang_dict_path
from backend.models import HanziSet
from tw_fuluzi import fuluzi


def is_has_letter(s):
    if re.findall(r'[A-Za-z]', s):
        return True
    else:
        return False


def variant_search(request):
    """
    异体字查询函数
    """

    q = request.GET.get('q', None)
    mark = request.GET.get('mark', None)

    # 如果缺少参数q就输出页面本身
    if (q is None):
        return render(request, 'variant_search.html')

    # 如果两个参数都有，输出别的页面
    if (q is not None and mark is not None):
        context = {}
        context["ext"] = q
        return render(request, 'variant_search.html', context)

    # 做检索操作
    result = HanziSet.objects.filter(
        Q(hanzi_char__contains=q) | Q(hanzi_pic_id=q)).order_by('source')
    ret = []
    for item in result:
        # 对于台湾异体字
        if (item.source == 2):
            d = {}
            d['source'] = 2
            d['content'] = []

            """
            #获得std_hanzi字段中的所有正字和这些正字包含的异体字
            """
            std_hanzi = item.std_hanzi.split(';')
            for item in std_hanzi:
                d1 = {}
                d1["stdchar"] = item
                if (is_has_letter(item)):
                    d1["type"] = 'pic'
                    d1["pic_url"] = get_pic_url_by_source_pic_name(2, item)
                else:
                    d1["type"] = 'char'
                d1["variant"] = []
                # 获得该类型正字的所有异体字
                result = HanziSet.objects.filter(
                    Q(std_hanzi__contains=item) & Q(source=2)).exclude(variant_type=0)
                for item in result:
                    d2 = {}
                    if (item.hanzi_char != ''):
                        d2["type"] = "char"
                        d2["text"] = item.hanzi_char
                    else:
                        d2["type"] = "pic"
                        d2["text"] = item.hanzi_pic_id
                        d2["pic_url"] = get_pic_url_by_source_pic_name(
                            2, item.hanzi_pic_id)

                    d1["variant"].append(d2)

                d['content'].append(d1)

            """
            #处理兼正字的情况
            """
            if item.as_std_hanzi != '' and item.as_std_hanzi[0] != '#':
                d1 = {}
                if item.hanzi_char != '':
                    d1["stdchar"] = item.hanzi_char
                    d1["type"] = 'char'
                elif item.hanzi_pic_id != '':
                    d1["stdchar"] = item.hanzi_pic_id
                    d1["type"] = 'pic'
                    d1["pic_url"] = get_pic_url_by_source_pic_name(
                        2, item.hanzi_pic_id)

                d1["variant"] = []
                # 获得该类型正字的所有异体字
                result = HanziSet.objects.filter(
                    Q(std_hanzi__contains=d1["stdchar"]) & Q(source=2)).exclude(variant_type=0)
                for item in result:
                    d2 = {}
                    if item.hanzi_char != '':
                        d2["type"] = "char"
                        d2["text"] = item.hanzi_char
                    else:
                        d2["type"] = "pic"
                        d2["text"] = item.hanzi_pic_id
                        d2["pic_url"] = get_pic_url_by_source_pic_name(
                            2, item.hanzi_pic_id)

                    d1["variant"].append(d2)

                d['content'].append(d1)

            ret.append(d)

        # 对于汉语大字典
        elif item.source == 3:
            # d = {}
            # d['source'] = 3
            # d['content'] = item.seq_id
            # d['pic_url'] = get_pic_url_by_source_pic_name(3,item.seq_id)
            # ret.append(d)

            d2 = {}
            if item.hanzi_char != '':
                d2["type"] = "char"
                d2["text"] = item.hanzi_char
            else:
                d2["type"] = "pic"
                d2["text"] = item.hanzi_pic_id
                d2["pic_url"] = get_pic_url_by_source_pic_name(
                    2, item.hanzi_pic_id)

            # 先检测ret中有没有汉语大字典信息，如果有就直接添加，如果没有要建立新的对象
            flag = False
            for item2 in ret:
                if item2['source'] == 3:
                    flag = True
                    break

            if flag:
                d = {}
                d['source'] = 3
                d['content'] = []
                d['content'].append(d2)
                ret.append(d)
            else:
                item2['content'].append(d2)

        # 对于高丽异体字
        elif item.source == 4:

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

            """
            #获得std_hanzi字段中的所有正字和这些正字包含的异体字
            """
            std_hanzi = item.std_hanzi.split(';')
            for item in std_hanzi:
                d1 = {}
                d1["stdchar"] = item
                if (is_has_letter(item)):
                    d1["type"] = 'pic'
                    d1["pic_url"] = get_pic_url_by_source_pic_name(4, item)
                else:
                    d1["type"] = 'char'
                d1["variant"] = []
                # 获得该类型正字的所有异体字
                result = HanziSet.objects.filter(
                    Q(std_hanzi__contains=item) & Q(source=4)).exclude(variant_type=0)
                for item in result:
                    d2 = {}
                    if (item.hanzi_char != ''):
                        d2["type"] = "char"
                        d2["text"] = item.hanzi_char
                    else:
                        d2["type"] = "pic"
                        d2["text"] = item.hanzi_pic_id
                        d2["pic_url"] = get_pic_url_by_source_pic_name(
                            4, item.hanzi_pic_id)

                    d1["variant"].append(d2)

                d['content'].append(d1)

            """
            #处理兼正字的情况
            """
            if (item.as_std_hanzi != '' and item.as_std_hanzi[0] != '#'):
                d1 = {}
                if (item.hanzi_char != ''):
                    d1["stdchar"] = item.hanzi_char
                    d1["type"] = 'char'
                elif (item.hanzi_pic_id != ''):
                    d1["stdchar"] = item.hanzi_pic_id
                    d1["type"] = 'pic'
                    d1["pic_url"] = get_pic_url_by_source_pic_name(
                        4, item.hanzi_pic_id)

                d1["variant"] = []
                # 获得该类型正字的所有异体字
                result = HanziSet.objects.filter(
                    Q(std_hanzi__contains=d1["stdchar"]) & Q(source=4)).exclude(variant_type=0)
                for item in result:
                    d2 = {}
                    if (item.hanzi_char != ''):
                        d2["type"] = "char"
                        d2["text"] = item.hanzi_char
                    else:
                        d2["type"] = "pic"
                        d2["text"] = item.hanzi_pic_id
                        d2["pic_url"] = get_pic_url_by_source_pic_name(
                            4, item.hanzi_pic_id)

                    d1["variant"].append(d2)

                d['content'].append(d1)

            ret.append(d)

        elif (item.source == 5):

            d2 = {}
            if (item.hanzi_char != ''):
                d2["type"] = "char"
                d2["text"] = item.hanzi_char
            else:
                d2["type"] = "pic"
                d2["text"] = item.hanzi_pic_id
                d2["pic_url"] = get_pic_url_by_source_pic_name(
                    2, item.hanzi_pic_id)

            # 先检测ret中有没有敦煌俗字典信息，如果有就直接添加，如果没有要建立新的对象
            flag = False
            for item2 in ret:
                if item2['source'] == 5:
                    flag = True
                    break

            if flag:
                d = {}
                d['source'] = 5
                d['content'] = []
                d['content'].append(d2)
                ret.append(d)
            else:
                item2['content'].append(d2)

    if len(ret) == 0:
        return HttpResponse("none")
    else:
        r = json.dumps(ret, ensure_ascii=False)
        return HttpResponse(r, content_type="application/json")


def get_tw_page(code_list):
    """
    对输入的列表进行处理，返回一个新列表
    比如，如果输入列表是["aaa-001","bbb"]
    那么，返回的列表是["aaa","bbb"]
    """
    tmp_list = []
    for item in code_list:
        if (item.find('-') != -1):
            tmp_list.append(item.split('-')[0])
        else:
            tmp_list.append(item)
    return tmp_list


def get_tw_iframe_up(code_list):
    """
    构造上窗格中iframe的src属性，放在list中返回
    输入参数为一个list，包含台湾异体字的图片ID
    """
    base = 'https://s3.cn-north-1.amazonaws.com.cn/yitizi'
    tmp_list = []
    for item in code_list:
        # 如果不是附录字
        if fuluzi.count(item) == 0:

            # 构造模板路径
            item = item.lower()
            first_letter = item[0].lower()
            up = base + '/yiti' + first_letter + '/w' + first_letter + '/w' + item + '.htm'
            tmp_list.append(up)

        else:
            item = item.lower()
            first_letter = item[0].lower()
            up = base + '/yiti' + first_letter + '/w' + first_letter + '/w' + item + '.htm'
            tmp_list.append(up)

    return tmp_list


def get_tw_iframe_left(code_list):
    """
    构造左窗格中iframe的src属性，放在list中返回
    输入参数为一个list，包含台湾异体字的图片ID
    """
    tmp_list = []
    base = 'https://s3.cn-north-1.amazonaws.com.cn/yitizi'
    for item in code_list:
        # 如果不是附录字
        if fuluzi.count(item) == 0:

            # 构造模板路径
            item = item.lower()
            first_letter = item[0].lower()
            left = base + '/yiti' + first_letter + '/' + \
                first_letter + '_std/' + item + '.htm'
            tmp_list.append(left)

        else:
            item = item.lower()
            first_letter = item[0].lower()
            left = base + '/yiti' + first_letter + '/' + \
                first_letter + '_std/' + item + '.htm'
            tmp_list.append(left)

    return tmp_list


def get_tw_iframe_right(code_list):
    """
    构造右窗格中iframe的src属性，放在list中返回
    输入参数为一个list，包含台湾异体字的图片ID
    """
    tmp_list = []
    base = 'https://s3.cn-north-1.amazonaws.com.cn/yitizi'
    for item in code_list:
        # 如果不是附录字
        if fuluzi.count(item) == 0:

            # 构造模板路径
            item = item.lower()
            first_letter = item[0].lower()
            right = base + '/yiti' + first_letter + \
                '/s' + first_letter + '/s' + item + '.htm'
            tmp_list.append(right)

        else:
            item = item.lower()
            first_letter = item[0].lower()
            right = base + '/yiti' + first_letter + \
                '/s' + first_letter + '/s' + item + '.htm'
            tmp_list.append(right)

    return tmp_list


def get_tw_url(code_list):
    """
    输入参数：台湾异体字ID数组，放在list中
    输出数据：台湾异体字在台湾网站的URL，放在list中返回
    """
    tmp_list = []
    for item in code_list:

        # 如果不是附录字
        if fuluzi.count(item) == 0:
            first_letter = item[0].lower()
            url = 'http://dict.variants.moe.edu.tw/yiti' + \
                first_letter + '/fr' + first_letter + '/fr' + item + '.htm'
        else:
            first_letter = item[0].lower()
            url = 'http://dict.variants.moe.edu.tw/yiti' + \
                first_letter + '/ur' + first_letter + '/ur' + item + '.htm'
        tmp_list.append(url)
    return tmp_list


def get_gl_url(char):
    """
    简单地输出高丽异体字的原始查询网址
    """
    return 'http://kb.sutra.re.kr/ritk_eng/etc/chinese/chineseBitSearch.do'


def get_hy_page(text):
    """
    输入参数：页码字符串，比如200-14，表示200页中的第14个字
    输出数据：页码，如上边的200
    """
    return text.split('-')[0]


def variant_detail(request):
    """
    输出显示异体字综合信息的网页
    """
    source = request.GET['source']  # char or pic
    kind = request.GET['type']  # char or pic
    text = request.GET['text']  # 可能是文字，也可能是图片字的文件名

    TW = {}  # 如果属于台湾异体字，其编码存入数组TW_char_addr
    HY = {}  # 如果属于汉语大字典，其页码存入变量HY
    GL = {}  # 如果属于高丽异体字，则找出对应正字的所有异体字，存入glyitizi
    DH = {}  # 如果属于敦煌俗字典，其页码存入变量DH_char_page、

    result = HanziSet.objects.filter(Q(hanzi_char__contains=text) | Q(
        hanzi_pic_id__exact=text)).order_by('source')

    for item in result:
        # 得到台湾字的信息
        if (item.source == 2):
            if (item.variant_type == 0):  # 如果是正字

                TW['dict'] = "台湾异体字"
                TW['type'] = "正字"
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

            elif (item.variant_type == 1):  # 如果是狭义异体字

                TW['dict'] = "台湾异体字"
                TW['type'] = "狭义异体字"
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
        elif (item.source == 3):
            HY['dict'] = "汉语大字典"
            HY['type'] = "正字"
            HY['addr'] = item.seq_id
            HY['page'] = ''
            if (len(get_hy_page(item.seq_id)) == 3):
                HY['page'] = get_hanyu_dict_path() + '0' + \
                    get_hy_page(item.seq_id) + '.png'
            elif (len(get_hy_page(item.seq_id)) == 4):
                HY['page'] = get_hanyu_dict_path(
                ) + get_hy_page(item.seq_id) + '.png'
            HY['zhengzhi'] = item.hanzi_char
            continue

        # 得到高丽异体字的信息。首先得到正字，再根据正字得到对应的异体字。
        # 对char型的高丽字来说，他本身就是正字
        elif (item.source == 4):
            # 如果已经有记录了，就返回，以免信息多余
            # if len(GL)>0:
            # 	continue
            obj = HanziSet.objects.filter(Q(source=4) & (
                Q(hanzi_char__contains=text) | Q(hanzi_pic_id__exact=text))).first()
            result = HanziSet.objects.filter(Q(source=4) & Q(
                std_hanzi=obj.std_hanzi)).exclude(hanzi_pic_id='')
            vraiant = []
            for item in result:
                t = {}
                t['pic_id'] = item.hanzi_pic_id
                t['pic_url'] = get_pic_url_by_source_pic_name(
                    4, item.hanzi_pic_id)
                vraiant.append(t)

            GL['dict'] = "高丽异体字"
            if (obj.variant_type == 0):  # 如果是正字
                GL['type'] = "正字"
            elif (obj.variant_type == 1):
                GL['type'] = "狭义异体字"
            GL['url'] = get_gl_url(text)
            GL['zhengzhi'] = obj.std_hanzi
            GL['vraiant'] = vraiant
            continue

        # 得到敦煌俗字典中的信息。处理起来比较简单。得到页码即可。
        elif (item.source == 5):
            DH['dict'] = "敦煌俗字典"
            DH['type'] = "正字"
            DH['addr'] = item.seq_id
            DH['page'] = get_dunhuang_dict_path() + item.seq_id + '.png'
            DH['zhengzhi'] = item.hanzi_char
            continue

    context = {}
    context['source'] = source
    context['type'] = kind
    context['text'] = text
    if (kind == 'pic'):
        context['pic_url'] = get_pic_url_by_source_pic_name(int(source), text)

    context['TW'] = TW
    context['HY'] = HY
    context['GL'] = GL
    context['DH'] = DH
    return render(request, 'hanzi_detail.html', context)
