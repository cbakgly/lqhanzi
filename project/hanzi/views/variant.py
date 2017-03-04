# coding=utf-8
from __future__ import unicode_literals
import json
import re
import operator
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from backend.utils import get_pic_url_by_source_pic_name
from backend.utils import get_hanyu_dict_path
from backend.utils import get_dunhuang_dict_path
from backend.models import HanziSet
from backend.enums import SOURCE_ENUM
from backend.enums import VARIANT_TYPE_INVERSE
from tw_fuluzi import fuluzi


def variant_search(request):
    """
    异体字检索页面
    """
    return render(request, 'variant_search.html', {'q': request.GET.get('q', None)})


def ajax_variant_search(request):
    """
    异体字检索。
    用户可输入文字或图片字编码。文字和图片字都可能因来源不同而有多条记录，从而对应多重身份，包括hanzi_char/hanzi_pic_id/inter_dict_dup_hanzi/korean_dup_hanzi。
    对于台湾异体字和高丽异体字而言，需要进一步根据所属正字去查找该正字以及正字包含的其他异体字，检索结果需要根据来源和正字进行分类展示。
    对于汉语大字典和敦煌俗字典而言，由于没有正异关系，则只需要显示字头信息即可。
    Unicode不参与异体字检索，可忽略。
    :return: json字符串，格式：
    {
        2: [  # 2表示来源于台湾异体字
            # 每个dict都是一个正字和正字对应的所有异体字的集合
            {source/hanzi_char/hanzi_pic_id/pic_url/std_hanzi/variant_type/variants[]},
            {source/hanzi_char/hanzi_pic_id/pic_url/std_hanzi/variant_type/variants[]},
        ],
        3: [...]
    }
    """
    q = request.GET.get('q', None)
    cnt = HanziSet.objects.filter(Q(hanzi_char__contains=q) | Q(hanzi_pic_id=q) | Q(seq_id__regex='^' + q + '(;|$)')).order_by('source').count()
    if not q or cnt == 0:
        return JsonResponse({'q': q, 'empty': True})

    hanzi_codes = ''  # 查询异体字的多重身份
    source_std_hanzis = {SOURCE_ENUM['taiwan']: [], SOURCE_ENUM['korean']: []}
    ret = {SOURCE_ENUM['taiwan']: [], SOURCE_ENUM['hanyu']: [], SOURCE_ENUM['korean']: [], SOURCE_ENUM['dunhuang']: []}  # 初始化结果集
    hanzi_set = HanziSet.objects.filter(Q(hanzi_char__contains=q) | Q(hanzi_pic_id=q) | Q(seq_id__regex='^' + q + '(;|$)')).order_by('source').values(
        'source', 'hanzi_char', 'hanzi_pic_id', 'std_hanzi', 'variant_type', 'inter_dict_dup_hanzi', 'korean_dup_hanzi')
    hanzi_set = list(hanzi_set)
    for hanzi in hanzi_set:
        hanzi_codes += hanzi['hanzi_char'] + ';' + hanzi['hanzi_pic_id'] + ';' + hanzi['inter_dict_dup_hanzi'] + ';' + hanzi['korean_dup_hanzi']
        if hanzi['source'] == SOURCE_ENUM['taiwan']:  # 台湾异体字
            if not hanzi['std_hanzi'] in source_std_hanzis[SOURCE_ENUM['taiwan']]:
                ret[SOURCE_ENUM['taiwan']] += __get_variants_by_std_hanzi(hanzi['std_hanzi'], SOURCE_ENUM['taiwan'])
                source_std_hanzis[SOURCE_ENUM['taiwan']].append(hanzi['std_hanzi'])
            if hanzi['inter_dict_dup_hanzi']:
                ret[SOURCE_ENUM['korean']] += __get_variants_by_hanzi_code(hanzi['inter_dict_dup_hanzi'], SOURCE_ENUM['korean'])

        if hanzi['source'] == SOURCE_ENUM['korean']:  # 高丽异体字
            if not hanzi['std_hanzi'] in source_std_hanzis[SOURCE_ENUM['korean']]:
                ret[SOURCE_ENUM['korean']] += __get_variants_by_std_hanzi(hanzi['std_hanzi'], SOURCE_ENUM['korean'])
                source_std_hanzis[SOURCE_ENUM['korean']].append(hanzi['std_hanzi'])
            if hanzi['korean_dup_hanzi']:
                ret[SOURCE_ENUM['korean']] += __get_variants_by_hanzi_code(hanzi['korean_dup_hanzi'], SOURCE_ENUM['korean'])
            if hanzi['inter_dict_dup_hanzi']:
                ret[SOURCE_ENUM['taiwan']] += __get_variants_by_hanzi_code(hanzi['inter_dict_dup_hanzi'], SOURCE_ENUM['taiwan'])

        if hanzi['source'] == SOURCE_ENUM['hanyu']:  # 汉语大字典
            hanzi['pic_url'] = get_pic_url_by_source_pic_name(SOURCE_ENUM['hanyu'], hanzi['hanzi_pic_id'])
            ret[SOURCE_ENUM['hanyu']] += [hanzi]

        if hanzi['source'] == SOURCE_ENUM['dunhuang']:  # 敦煌俗字典
            hanzi['pic_url'] = get_pic_url_by_source_pic_name(SOURCE_ENUM['dunhuang'], hanzi['hanzi_pic_id'])
            ret[SOURCE_ENUM['dunhuang']] += [hanzi]

    hanzi_codes = re.sub(r";+", r";", hanzi_codes).strip(';')
    ret['hanzi_codes'] = list(set(hanzi_codes.split(';')))

    return JsonResponse({'q': q, 'empty': False, 'data': ret})


def __get_variants_by_hanzi_code(hanzi_code, source):
    """
    查询文字或图片字对应的正字及该正字对应的所有异体字
    :param hanzi_code:文字(hanzi_char)或图片字编码(hanzi_pic_id)
    :param source:来源
    """
    hanzi_set = list(HanziSet.objects.filter(Q(hanzi_char__contains=hanzi_code) | Q(hanzi_pic_id=hanzi_code)).filter(Q(source=source)).values('std_hanzi'))
    if len(hanzi_set) == 0 or not hanzi_set[0]['std_hanzi']:
        return []
    else:
        return __get_variants_by_std_hanzi(hanzi_set[0]['std_hanzi'], source)


def __get_variants_by_std_hanzi(std_hanzis, source):
    """
    查询正字字符串对应的所有异体字
    :param std_hanzis:正字字符串，以;分隔
    :param source:来源
    :return: list：
    [
        # 每个dict都是一个正字和正字对应的所有异体字的集合
        {source/hanzi_char/hanzi_pic_id/pic_url/std_hanzi/variant_type/variants[]},
        {source/hanzi_char/hanzi_pic_id/pic_url/std_hanzi/variant_type/variants[]},
    ]
    """
    if not std_hanzis:
        return []

    # 查询正字字符串对应的所有异体字
    dicts = {}
    query_list = []
    for std_hanzi in std_hanzis.split(';'):
        query_list.append(Q(std_hanzi__contains=std_hanzi))
        dicts[std_hanzi] = {}
    variants = HanziSet.objects.filter(Q(source=source)).filter(reduce(operator.or_, query_list)).values(
        'source', 'hanzi_char', 'hanzi_pic_id', 'std_hanzi', 'variant_type')
    variants = list(variants)

    # 按所属正字进行分类
    for v in variants:
        v["pic_url"] = get_pic_url_by_source_pic_name(source, v['hanzi_pic_id'])
        if v['hanzi_char'] in dicts:
            dicts[v['hanzi_char']].update(v)
        if v['hanzi_pic_id'] in dicts:
            dicts[v['hanzi_pic_id']].update(v)

        v_std_hanzi = v['std_hanzi'].replace(v['hanzi_char'], '')
        v_std_hanzi = v_std_hanzi.replace(v['hanzi_pic_id'], '')
        v_std_hanzi_belong_search = filter(lambda x: x in std_hanzis.split(';'), v_std_hanzi.split(';'))  # 求v所属正字
        for d in v_std_hanzi_belong_search:  # 将v分配到所属正字
            if 'variants' in dicts[d]:
                dicts[d]['variants'].append(v)
            else:
                dicts[d]['variants'] = [v]

    return dicts.values()


def variant_detail(request):
    """
    异体字综合信息的页面。
    用户可输入文字或图片字编码。文字和图片字都可能因来源不同而有多条记录，从而对应多重身份，包括hanzi_char/hanzi_pic_id/inter_dict_dup_hanzi/korean_dup_hanzi。
    台湾异体字、高丽异体字由于有重复关系，可能存在多条记录。汉语大字典和敦煌俗字典则最多有一条记录。Unicode不参与异体字检索，可忽略。
    """
    q = request.GET.get('q', None)
    cnt = HanziSet.objects.filter(Q(hanzi_char__contains=q) | Q(hanzi_pic_id=q) | Q(seq_id__regex='^' + q + '(;|$)')).order_by('source').count()
    if not q or cnt == 0:
        return render(request, 'hanzi_detail.html', {'q': q, 'empty': True})

    hanzi_set = HanziSet.objects.filter(Q(hanzi_char__contains=q) | Q(hanzi_pic_id=q) | Q(seq_id__regex='^' + q + '(;|$)')).order_by('source').values(
        'source', 'hanzi_char', 'hanzi_pic_id', 'std_hanzi', 'seq_id', 'variant_type', 'inter_dict_dup_hanzi', 'korean_dup_hanzi')

    ret = {'q': q, 'empty': False, 'taiwan': {}, 'hanyu': {}, 'korean': {}, 'dunhuang': {}}  # 初始化结果集
    for hanzi in list(hanzi_set):
        if hanzi['source'] == SOURCE_ENUM['taiwan']:  # 台湾异体字
            ret['taiwan'] = {
                'variant_type': VARIANT_TYPE_INVERSE[hanzi['variant_type']],
                'std_hanzi': hanzi['std_hanzi'],
                'positions': hanzi['seq_id'].split(';'),  # 位置信息
                'origin_positions': get_tw_url(hanzi['seq_id']),  # 原始出处
            }

            if hanzi['inter_dict_dup_hanzi']:  # 字典间去重
                hanzi_korean = HanziSet.objects.filter(Q(source=SOURCE_ENUM['korean']) & Q(hanzi_pic_id=hanzi['inter_dict_dup_hanzi'])).values(
                    'source', 'hanzi_char', 'hanzi_pic_id', 'std_hanzi', 'seq_id', 'variant_type')
                hanzi_korean = list(hanzi_korean)
                if not hanzi_korean:
                    hanzi = hanzi_korean[0]
                    positions = hanzi['hanzi_pic_id']
                    if not positions:
                        positions = hanzi['hanzi_char']
                    ret['korean'] = {
                        'variant_type': VARIANT_TYPE_INVERSE[hanzi['variant_type']],
                        'std_hanzi': hanzi['std_hanzi'],
                        'positions': positions.split(';'),
                        'origin_positions': get_kr_url(positions),
                    }

        if hanzi['source'] == SOURCE_ENUM['korean']:  # 高丽异体字
            positions = hanzi['hanzi_pic_id']
            if not positions:
                positions = hanzi['hanzi_char']
            if not hanzi['korean_dup_hanzi']:  # 高丽异体字内部去重
                positions += ';' + hanzi['korean_dup_hanzi']
            ret['korean'] = {
                'variant_type': VARIANT_TYPE_INVERSE[hanzi['variant_type']],
                'std_hanzi': hanzi['std_hanzi'],
                'positions': positions.split(';'),
                'origin_positions': get_kr_url(positions),
            }
            if hanzi['inter_dict_dup_hanzi']:  # 字典间去重
                hanzi_taiwan = HanziSet.objects.filter(Q(source=SOURCE_ENUM['taiwan']) & Q(hanzi_pic_id=hanzi['inter_dict_dup_hanzi'])).values(
                    'source', 'hanzi_char', 'hanzi_pic_id', 'std_hanzi', 'seq_id', 'variant_type')
                hanzi_taiwan = list(hanzi_taiwan)
                if not hanzi_taiwan:
                    hanzi = hanzi_taiwan[0]
                    ret['taiwan'] = {
                        'variant_type': VARIANT_TYPE_INVERSE[hanzi['variant_type']],
                        'std_hanzi': hanzi['std_hanzi'],
                        'positions': hanzi['seq_id'].split(';'),
                        'origin_positions': get_tw_url(hanzi['seq_id']),  # 原始出处
                    }

        if hanzi['source'] == SOURCE_ENUM['hanyu']:  # 汉语大字典
            ret['hanyu'] = {
                'positions': hanzi['seq_id'],
                'image_url': get_zh_image_url(hanzi['seq_id']),
            }

        if hanzi['source'] == SOURCE_ENUM['dunhuang']:  # 敦煌俗字典
            ret['dunhuang'] = {
                'positions': hanzi['seq_id'],
                'image_url': get_dh_image_url(hanzi['seq_id']),
            }

    if hanzi_set[0]['hanzi_char']:  # 字头
        ret['hanzi_char'] = hanzi_set[0]['hanzi_char']
    else:
        ret['hanzi_pic_id'] = hanzi_set[0]['hanzi_pic_id']
        ret['pic_url'] = get_pic_url_by_source_pic_name(hanzi_set[0]['source'], hanzi_set[0]['hanzi_pic_id'])

    return render(request, 'variant_detail.html', ret)


def get_tw_url(seq_id):
    """
    获取原始台湾异体字网站的url
    :param seq_id: 位置信息，对应于数据库表中的seq_id字段
    """
    ret = []
    for s in seq_id.split(';'):
        if s in fuluzi:
            url = 'http://dict.variants.moe.edu.tw/yiti' + s[0].lower() + '/ur' + s[0].lower() + '/ur' + s.split('-')[0].lower() + '.htm'
        else:
            url = 'http://dict.variants.moe.edu.tw/yiti' + s[0].lower() + '/fr' + s[0].lower() + '/fr' + s.split('-')[0].lower() + '.htm'
        ret.append({'seq_id': s, 'url': url})
    return ret


def get_kr_url(seq_id):
    """
    获取原始高丽异体字网站的url
    """
    ret = []
    for s in seq_id.lower().split(';'):
        url = 'http://kb.sutra.re.kr/ritk_eng/etc/chinese/chineseBitSearch.do'
        ret.append({'seq_id': s, 'url': url})
    return ret


def get_zh_image_url(seq_id):
    """
    获取《汉语大字典》图片url
    """
    return get_hanyu_dict_path() + seq_id.split('-')[0] + ".png"


def get_dh_image_url(seq_id):
    """
    获取《敦煌俗字典》图片url
    """
    return get_dunhuang_dict_path() + seq_id.split('-')[0] + ".png"


def variant_detail2(request):
    """
    异体字综合信息的页面。
    """
    source = request.GET['source']  # char or pic
    kind = request.GET['type']  # char or pic
    text = request.GET['text']  # 可能是文字，也可能是图片字的文件名

    TW = {}  # 如果属于台湾异体字，其编码存入数组TW_char_addr
    HY = {}  # 如果属于汉语大字典，其页码存入变量HY
    GL = {}  # 如果属于高丽异体字，则找出对应正字的所有异体字，存入glyitizi
    DH = {}  # 如果属于敦煌俗字典，其页码存入变量DH_char_page、

    result = HanziSet.objects.filter(Q(hanzi_char__contains=text) | Q(hanzi_pic_id__exact=text)).order_by('source')

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
            GL['url'] = get_kr_url(text)
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
    base = 'http://s3.cn-north-1.amazonaws.com.cn/yitizi'
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
    base = 'http://s3.cn-north-1.amazonaws.com.cn/yitizi'
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
    base = 'http://s3.cn-north-1.amazonaws.com.cn/yitizi'
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


def get_hy_page(text):
    """
    输入参数：页码字符串，比如200-14，表示200页中的第14个字
    输出数据：页码，如上边的200
    """
    return text.split('-')[0]
