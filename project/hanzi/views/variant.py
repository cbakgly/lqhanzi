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


def help(request):
    """
    帮助页面
    """
    return render(request, 'hanzi_help.html')


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
    if( len(ret[SOURCE_ENUM['taiwan']])==0 and
        len(ret[SOURCE_ENUM['korean']])==0 and
        len(ret[SOURCE_ENUM['hanyu']])==0 and
        len(ret[SOURCE_ENUM['dunhuang']])==0 ):
        return JsonResponse({'q': q, 'empty': True, 'data': ret})
    else:
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
    return get_hanyu_dict_path() + '0' + seq_id.split('-')[0] + ".png"


def get_dh_image_url(seq_id):
    """
    获取《敦煌俗字典》图片url
    """
    return get_dunhuang_dict_path() + seq_id.split('-')[0] + ".png"
