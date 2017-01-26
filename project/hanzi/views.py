# coding=utf-8

import json
import re
from django.core.serializers import serialize
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from backend.utils import get_pic_url_by_source_pic_name
from backend.utils import get_dunhuang_dict_path
from backend.utils import get_hanyu_dict_path
from backend.models import HanziParts, HanziSet, Radical
from appendix_hanzi import fuluzi


# 取出附录字，存入list变量
# file="hanzi/fuluzi.txt"
# fp=open(file)
# fuluzi=[]
# for line in fp.readlines():
#     line = line.replace("[","")
#     line = line.replace("]","")
#     line = line.replace("\"","")
#     line = line.replace(" ","")
#     fuluzi.extend(line.split(","))
# fp.close()


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


# p = re.compile(r'^[^,\. \?]*$') #中括号里面先写个^表示非, 然后, 后面写你要过滤的符号.过滤了逗号, 句号, 空格, 问号四种.
# result = p.match(line)  #如果匹配的结果不为空, 说明这行是符合规则的, 没有这些指定字符的.
# if result:
#     pass
#     #该行无指定符号
# else:
#     pass
#     #该行有指定符号









'''
取部件函数
'''


@csrf_exempt
def get_parts():
    parts = HanziParts.objects.all().order_by('strokes', 'stroke_order')
    a = serialize("json", parts, ensure_ascii=False)
    b = json.loads(a)
    c = []
    for item in b:
        c.append(item['fields'])

    flag = 0
    length = len(c)
    for i in range(length):
        if (c[i]['strokes'] != flag):
            flag = c[i]['strokes']
            c.insert(i, {"flag": flag})
    return c


'''
取部首函数
'''


def get_radical():
    queryset = Radical.objects.all()
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


# Entry.objects.get(title__regex=r'^(An?|The) +')
@csrf_exempt
def stroke_ajax_search(request):
    # 得到参数
    q = request.GET.get('q', None)
    order = request.GET.get('order', None)
    page_size = request.GET.get('page_size', None)
    page_num = request.GET.get('page_num', None)

    # 参数不足四个就参数出错信息
    if (q == None or order == None or page_size == None or page_num == None):
        return HttpResponse("parameters is invalid")

    # 较验参数有效性


    page_size = int(page_size)
    page_num = int(page_num)

    if (order == '1'):
        total = HanziSet.objects.filter(Q(mix_split__contains=q)).count()
        pages = total / page_size + 1
        result = HanziSet.objects.filter(Q(mix_split__contains=q)).order_by('source')[(page_num - 1) * page_size: page_num * page_size]

        # result = HanziSet.objects.filter( Q(mix_split__contains=q) ).order_by('source')#[20:30]
        a = serialize("json", result, ensure_ascii=False)
        b = json.loads(a)
        c = []
        for item in b:
            c.append(item['fields'])
        for item in c:
            if (item['hanzi_pic_id'] != ""):
                item['pic_url'] = get_pic_url_by_source_pic_name(item['source'], item['hanzi_pic_id'])

        r = {}
        r['q'] = q
        r['order'] = order
        r['page_num'] = page_num
        r['pages'] = pages
        r['page_size'] = page_size
        r['result'] = c

        d = json.dumps(r, ensure_ascii=False)

        # write_log("stroke_search.txt",d)

        return HttpResponse(d, content_type="application/json")

    elif (order == '2'):
        pass


'''
异体字查询函数
'''


@csrf_exempt
def variant_search(request):
    # 得到参数
    q = request.GET.get('q', None)

    # 较验参数有效性


    # 如果缺少参数q就输出页面本身
    if (q == None):
        return render(request, 'variant_search.html')

    # 做检索操作
    result = HanziSet.objects.filter(Q(hanzi_char=q) | Q(hanzi_pic_id=q)).order_by('source')

    # 返回值是一个list，里边包含若干字典变量，每个字典又包含很复杂的内容，见下面结构
    # ret[]:
    # [
    # 	{ source:2,
    # 	  content:{
    # 				{stdchar:aaa
    # 				 type:char
    # 				 variant:[
    # 				 		  {type:pic,text:aaa},
    # 				 		  {type:char,text:bbb},
    # 				 		  {type:char,text:ccc},
    # 				 		 ]
    # 				 }
    # 				{stdchar:bbb
    # 				 type:char
    # 				 variant:[
    # 				 		  {type:pic,text:aaa},
    # 				 		  {type:char,text:bbb},
    # 				 		  {type:char,text:ccc},
    # 				 		 ]
    # 				 }
    # 				{stdchar:ccc
    # 				 type:pic
    # 				 variant:[
    # 				 		  {type:pic,text:aaa},
    # 				 		  {type:char,text:bbb},
    # 				 		  {type:char,text:ccc},
    # 				 		 ]
    # 				 }
    # 			  }
    #  }
    #
    # 	{ source:4,
    # 	  content:{
    # 				{stdchar:aaa
    # 				 type:char
    # 				 variant:[
    # 				 		  {type:pic,text:aaa},
    # 				 		  {type:char,text:bbb},
    # 				 		  {type:char,text:ccc},
    # 				 		 ]
    # 				 }
    # 				{stdchar:bbb
    # 				 type:char
    # 				 variant:[
    # 				 		  {type:pic,text:aaa},
    # 				 		  {type:char,text:bbb},
    # 				 		  {type:char,text:ccc},
    # 				 		 ]
    # 				 }
    # 				{stdchar:ccc
    # 				 type:pic
    # 				 variant:[
    # 				 		  {type:pic,text:aaa},
    # 				 		  {type:char,text:bbb},
    # 				 		  {type:char,text:ccc},
    # 				 		 ]
    # 				 }
    # 			  }
    #  }
    # ]


    ret = []
    for item in result:
        # 对于台湾异体字
        if (item.source == 2):
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
                if (is_has_letter(item)):
                    d1["type"] = 'pic'
                    d1["pic_url"] = get_pic_url_by_source_pic_name(2, item)
                else:
                    d1["type"] = 'char'
                d1["variant"] = []
                # 获得该类型正字的所有异体字
                result = HanziSet.objects.filter(Q(std_hanzi__contains=item) & Q(source=2)).exclude(variant_type=0)
                for item in result:
                    d2 = {}
                    if (item.hanzi_char != ''):
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
            if (item.as_std_hanzi != '' and item.as_std_hanzi[0] != '#'):
                d1 = {}
                if (item.hanzi_char != ''):
                    d1["stdchar"] = item.hanzi_char
                    d1["type"] = 'char'
                elif (item.hanzi_pic_id != ''):
                    d1["stdchar"] = item.hanzi_pic_id
                    d1["type"] = 'pic'
                    d1["pic_url"] = get_pic_url_by_source_pic_name(2, item.hanzi_pic_id)

                d1["variant"] = []
                # 获得该类型正字的所有异体字
                result = HanziSet.objects.filter(Q(std_hanzi__contains=d1["stdchar"]) & Q(source=2)).exclude(variant_type=0)
                for item in result:
                    d2 = {}
                    if (item.hanzi_char != ''):
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
        elif (item.source == 3):
            d = {}
            d['source'] = 3
            d['content'] = item.seq_id
            d['pic_url'] = get_pic_url_by_source_pic_name(3, item.seq_id)
            ret.append(d)

        # 对于高丽异体字
        elif (item.source == 4):
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
                if (is_has_letter(item)):
                    d1["type"] = 'pic'
                    d1["pic_url"] = get_pic_url_by_source_pic_name(4, item)
                else:
                    d1["type"] = 'char'
                d1["variant"] = []
                # 获得该类型正字的所有异体字
                result = HanziSet.objects.filter(Q(std_hanzi__contains=item) & Q(source=4)).exclude(variant_type=0)
                for item in result:
                    d2 = {}
                    if (item.hanzi_char != ''):
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
            if (item.as_std_hanzi != '' and item.as_std_hanzi[0] != '#'):
                d1 = {}
                if (item.hanzi_char != ''):
                    d1["stdchar"] = item.hanzi_char
                    d1["type"] = 'char'
                elif (item.hanzi_pic_id != ''):
                    d1["stdchar"] = item.hanzi_pic_id
                    d1["type"] = 'pic'
                    d1["pic_url"] = get_pic_url_by_source_pic_name(4, item.hanzi_pic_id)

                d1["variant"] = []
                # 获得该类型正字的所有异体字
                result = HanziSet.objects.filter(Q(std_hanzi__contains=d1["stdchar"]) & Q(source=4)).exclude(variant_type=0)
                for item in result:
                    d2 = {}
                    if (item.hanzi_char != ''):
                        d2["type"] = "char"
                        d2["text"] = item.hanzi_char
                    else:
                        d2["type"] = "pic"
                        d2["text"] = item.hanzi_pic_id
                        d2["pic_url"] = get_pic_url_by_source_pic_name(4, item.hanzi_pic_id)

                    d1["variant"].append(d2)

                d['content'].append(d1)

            ret.append(d)

        elif (item.source == 5):
            d = {}
            d['source'] = 5
            d['content'] = item.seq_id
            d['pic_url'] = get_pic_url_by_source_pic_name(5, item.seq_id)
            ret.append(d)

    r = json.dumps(ret, ensure_ascii=False)
    # write_log("variant_search.txt",r)
    return HttpResponse(r, content_type="application/json")


# 输入参数为list，返回值也是list
# 输入参数必须是A00111-001 或者A00111这样的字符串
def get_page(code_list):
    tmp_list = []
    for item in code_list:
        if (item.find('-') != -1):
            tmp_list.append(item.split('-')[0])
        else:
            tmp_list.append(item)
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
    url = 'http://kb.sutra.re.kr/ritk_eng/etc/chinese/chineseBitSearch.do'
    return url


def get_hy_page(text):
    return text.split('-')[1]


def get_hy_mark(seq_id):
    return 'hy'


def get_dh_mark(seq_id):
    return 'dh'


# 第一个参数是所属字典，第二个是图片id
# 返回值：图片在静态文件中的路径，以static开头
# def get_pic_path(char_dict,pic_id):
# 	try:
# 		obj = HanziSet.objects.get( Q(source=char_dict ) & Q(hanzi_pic_id=pic_id) ) 

# 		path = ''
# 		if (char_dict == '2') :  			 	#如果是台湾图片
# 			forst_two_letter = pic_id[0:2]		#截取前两个字母
# 			path = '/static/tw/' + forst_two_letter + '/' + pic_id + '.png'
# 		elif (char_dict == '3'):					#如果是汉语大字典里的字
# 			path = '/static/hy/' + pic_id + '.png'
# 			print path
# 		elif (char_dict == '4') :   				#如果是高丽字典里的字
# 			if(obj.variant_type == 0):			#如果是正字
# 				path = '/static/gl/standard/' + pic_id + '.png'
# 			else:
# 				path = '/static/gl/variant/' + pic_id + '.png'
# 		elif (char_dict == '5'):		#如果是敦煌俗字典里的字
# 			path = '/static/dh/' + pic_id + '.png'
# 		else:
# 			pass
# 		return path		
# 	except:
# 		return ''


@csrf_exempt
def variant_detail(request):
    # text值可能是一个文字字，也可能是图片字的文件名
    source = request.GET['source']  # char or pic
    type = request.GET['type']  # char or pic
    text = request.GET['text']  # if char,char;or,pic_id

    TW = {}  # 如果属于台湾异体字，其编码存入数组TW_char_addr
    HY = {}  # 如果属于汉语大字典，其页码存入变量HY
    GL = {}  # 如果属于高丽异体字，则找出对应正字的所有异体字，存入glyitizi
    DH = {}  # 如果属于敦煌俗字典，其页码存入变量DH_char_page、

    result = HanziSet.objects.filter(Q(hanzi_char__exact=text) | Q(hanzi_pic_id__exact=text)).order_by('source')
    # result = HanziSet.objects.filter( Q(hanzi_char__contains =text) | Q(hanzi_pic_id__contains =text) ).order_by('source')
    # 得到台湾字的信息
    for item in result:
        if (item.source == 2):
            if (item.variant_type == 0):  # 如果是正字

                TW['dict'] = "台湾异体字"
                tmp_list = []
                tmp_list.append(item.seq_id)
                TW['addr'] = tmp_list
                TW['page'] = get_page(TW['addr'])
                TW['url'] = get_tw_url(TW['page'])

                TW['a'] = zip(TW['addr'], TW['url'])
                TW['tab'] = zip(TW['addr'], TW['page'])

                TW['zhengzhi'] = item.std_hanzi
                TW['mark'] = "正字"
                continue

            elif (item.variant_type == 1):  # 如果是狭义异体字

                TW['dict'] = "台湾异体字"

                tmp_list = []
                tmp_list.append(item.seq_id)
                TW['addr'] = tmp_list

                TW['page'] = get_page(TW['addr'])
                TW['url'] = get_tw_url(TW['page'])

                TW['a'] = zip(TW['addr'], TW['url'])
                TW['tab'] = zip(TW['addr'], TW['page'])

                TW['zhengzhi'] = item.std_hanzi
                TW['mark'] = "狭义异体字"
                continue

            elif (item.variant_type == 2):  # 如果是异体字兼正字

                TW['dict'] = "台湾异体字"
                TW['addr'] = item.seq_id.split(';')
                TW['addr'].append(item.as_std_hanzi)
                TW['page'] = get_page(TW['addr'])
                TW['url'] = get_tw_url(TW['page'])

                TW['a'] = zip(TW['addr'], TW['url'])
                TW['tab'] = zip(TW['addr'], TW['page'])

                TW['zhengzhi'] = item.std_hanzi + ';' + item.hanzi_char
                TW['mark'] = "异体字兼正字"
                continue

            elif (item.variant_type == 3):  # 如果是广义异体字

                TW['dict'] = "台湾异体字"
                TW['addr'] = item.seq_id.split(';')
                TW['page'] = get_page(TW['addr'])
                TW['url'] = get_tw_url(TW['page'])

                TW['a'] = zip(TW['addr'], TW['url'])
                TW['tab'] = zip(TW['addr'], TW['page'])

                TW['zhengzhi'] = item.std_hanzi
                TW['mark'] = "广义异体字"
                continue

            elif (item.variant_type == 4):
                continue


        # 得到汉语大字典中的信息。处理起来比较简单。得到页码即可。
        elif (item.source == 3):
            HY['dict'] = "汉语大字典"
            HY['addr'] = item.seq_id
            # HY['page'] = get_pic_url_by_source_pic_name(3,item.seq_id) #   get_hy_page(item.seq_id)

            HY['page_url'] = get_hanyu_dict_path() + get_hy_page(item.seq_id) + '.png'
            HY['zhengzhi'] = item.hanzi_char
            HY['mark'] = get_hy_mark(item.seq_id)
            continue

        # 得到高丽异体字的信息。首先得到正字，再根据正字得到对应的异体字。
        # 对char型的高丽字来说，他本身就是正字
        elif (item.source == 4):
            obj = HanziSet.objects.get(Q(source=4) & (Q(hanzi_char__exact=text) | Q(hanzi_pic_id__exact=text)))
            result = HanziSet.objects.filter(Q(source=4) & Q(std_hanzi=obj.std_hanzi)).exclude(hanzi_pic_id='')
            vraiant = []
            for item in result:
                t = {}
                t['pic_id'] = item.hanzi_pic_id
                t['pic_url'] = get_pic_url_by_source_pic_name(4, item.hanzi_pic_id)
                vraiant.append(t)

            GL['dict'] = "高丽异体字"
            # GL['addr'] = item.seq_id
            GL['url'] = get_gl_url(text)
            GL['zhengzhi'] = obj.std_hanzi
            # GL['zhengzhi_url'] = get_pic_url_by_source_pic_name(4,item.seq_id) #obj.std_hanzi
            GL['mark'] = ''
            GL['vraiant'] = vraiant
            continue

        # 得到敦煌俗字典中的信息。处理起来比较简单。得到页码即可。
        elif (item.source == 5):
            DH['dict'] = "敦煌俗字典"
            DH['addr'] = item.seq_id
            # DH['page'] = +item.seq_id
            DH['page_url'] = get_dunhuang_dict_path() + item.seq_id + '.png'

            DH['zhengzhi'] = item.hanzi_char
            DH['mark'] = get_dh_mark(item.seq_id)
            continue

    context = {}
    context['source'] = source
    context['type'] = type
    context['text'] = text
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

    source = int(source)
    page_size = int(page_size)
    page_num = int(page_num)

    total = HanziSet.objects.filter(Q(radical=q) & Q(source=source)).count()
    pages = total / page_size + 1
    result = HanziSet.objects.filter(Q(radical=q) & Q(source=source)).values('source', 'strokes', 'hanzi_char', 'hanzi_pic_id', 'mix_split', 'similar_parts').order_by('strokes')[(page_num - 1) * page_size: page_num * page_size]

    print type(result)

    a = []
    radical_strokes_num = Radical.objects.get(radical=q).strokes  # 部首笔画数
    for item in result:
        item['pic_url'] = get_pic_url_by_source_pic_name(source, item['hanzi_pic_id'])
        item['remain_strokes_num'] = item['strokes'] - radical_strokes_num
        a.append(item)

    b = {}
    b['q'] = q
    b['source'] = source
    b['page_num'] = page_num
    b['pages'] = pages
    b['page_size'] = page_size
    b['result'] = a

    d = json.dumps(b, ensure_ascii=False)

    # print d
    # write_log("dicts_search.txt",d)
    return HttpResponse(d, content_type="application/json")


# @csrf_exempt
# def show_iframe(request):

# 	#取出汉字代码
# 	tw_char_code = request.path.split('/')[3].encode("utf-8")

# 	#如果不是附录字
# 	if fuluzi.count( tw_char_code ) == 0:

# 		#构造模板路径
# 		tw_char_code = tw_char_code.lower()
# 		first_letter = tw_char_code[0].lower()
# 		up = '/hanzi/yitizi/yiti' + first_letter + '/w' + first_letter + '/w' + tw_char_code + '.htm'
# 		down = '/hanzi/yitizi/yiti' + first_letter + '/' + first_letter + '_std/' + tw_char_code + '.htm'
# 		right = '/hanzi/yitizi/yiti' + first_letter + '/s' + first_letter + '/s' + tw_char_code + '.htm'

# 	else:
# 		tw_char_code = tw_char_code.lower()
# 		first_letter = tw_char_code[0].lower()
# 		up = '/hanzi/yitizi/yiti' + first_letter + '/w' + first_letter + '/w' + tw_char_code + '.htm'
# 		down = '/hanzi/yitizi/yiti' + first_letter + '/fu' + first_letter + '/fu' + tw_char_code + '.htm'
# 		right = '/hanzi/yitizi/yiti' + first_letter + '/s' + first_letter + '/s' + tw_char_code + '.htm'


# 	context = {}
# 	context['up'] = up
# 	context['down'] = down
# 	context['right'] = right	
# 	return render(request, 'iframe.htm', context)  	




# @csrf_exempt
# def show_yitizi(request):
# 	path =  request.path.encode("utf-8")
# 	addr = path[7:len(path)]
# 	return render_to_response(addr)


# @csrf_exempt
# def variant2(request):
# 	return render(request, 'variant2.htm', context)  

'''
这个函数，里边的分页功能将由我自己写，不用Paginator
'''
# @csrf_exempt
# def check_by_bujian(request):
# 	page = 0
# 	page_size = 50
# 	if request.method == 'GET':
# 		q = request.GET['q']
# 		page  = int(request.GET['page']) # 获取页码
# 	elif request.method == 'POST':
# 		q = request.POST['q']
# 		page  = int(request.POST['page']) # 获取页码

# 	pages = HanziSet.objects.filter( Q(mix_split__contains=q)  ).count() / page_size + 1
# 	result = HanziSet.objects.filter( Q(mix_split__contains=q)  ).order_by('source')[(page-1)*page_size:page*page_size]
# 	for item in result:
# 		if( item.hanzi_pic_id != "" ):
# 			item.pic_url = get_pic_path( str(item.source),item.hanzi_pic_id ) 

# 	context = {}
# 	context['page'] = page
# 	context['pages'] = pages
# 	context['q'] = q
# 	context['result'] = result
# 	return render(request, 'checkresult.htm', context) 


'''
异体字查询页面
'''
# @csrf_exempt
# def variant(request):
# 	return render(request,'variant_search.html')


# '''
# 取部件函数，可以考虑用values()查询，以降低数据库负担
# '''
# @csrf_exempt
# def get_parts(request):
# 	parts = HanziParts.objects.all().order_by('strokes','stroke_order')#.order_by('stroke_order')#[0:10]
# 	a = serialize("json",parts,ensure_ascii=False)
# 	b = json.loads(a)
# 	c = []
# 	for item in b:
# 		c.append(item['fields'])
# 	d = json.dumps(c,ensure_ascii=False)
# 	# print d
# 	write_log("get_parts.txt",d)
# 	return HttpResponse(d,content_type="application/json")
# 	


# @csrf_exempt
# def strock_search(request):
# 	pages = 0
# 	page_size = 100

# 	q = request.GET['q']
# 	order = request.GET['order']
# 	page  = int(request.GET['page'])

# 	if order=='1':
# 		total = HanziSet.objects.filter( Q(mix_split__contains=q)  ).count()
# 		pages = total / page_size + 1
# 		result = HanziSet.objects.filter( Q(mix_split__contains=q)  ).order_by('source')[(page-1)*page_size:page*page_size]

# 		for item in result:
# 			if( item.hanzi_pic_id != "" ):
# 				item.pic_url = get_pic_path( str(item.source),item.hanzi_pic_id ) 

# 	elif order == 2:
# 		pass


# 	context = {}
# 	context['page'] = page
# 	context['pages'] = pages
# 	context['q'] = q
# 	context['total'] = total
# 	context['result'] = result
# 	return render(request, 'checkresult.htm', context) 

# Entry.objects.get(title__regex=r'^(An?|The) +')




# @csrf_exempt
# def show_iframe(request):

# 	#取出汉字代码
# 	tw_char_code = request.path.split('/')[3].encode("utf-8")

# 	#如果不是附录字
# 	if fuluzi.count( tw_char_code ) == 0:

# 		#构造模板路径
# 		tw_char_code = tw_char_code.lower()
# 		first_letter = tw_char_code[0].lower()
# 		up = '/hanzi/yitizi/yiti' + first_letter + '/w' + first_letter + '/w' + tw_char_code + '.htm'
# 		down = '/hanzi/yitizi/yiti' + first_letter + '/' + first_letter + '_std/' + tw_char_code + '.htm'
# 		right = '/hanzi/yitizi/yiti' + first_letter + '/s' + first_letter + '/s' + tw_char_code + '.htm'

# 	else:
# 		tw_char_code = tw_char_code.lower()
# 		first_letter = tw_char_code[0].lower()
# 		up = '/hanzi/yitizi/yiti' + first_letter + '/w' + first_letter + '/w' + tw_char_code + '.htm'
# 		down = '/hanzi/yitizi/yiti' + first_letter + '/fu' + first_letter + '/fu' + tw_char_code + '.htm'
# 		right = '/hanzi/yitizi/yiti' + first_letter + '/s' + first_letter + '/s' + tw_char_code + '.htm'


# 	context = {}
# 	context['up'] = up
# 	context['down'] = down
# 	context['right'] = right	
# 	return render(request, 'iframe.htm', context)  	

# '''
# 取部首函数，可以考虑用values()查询，以降低数据库负担
# '''
# @csrf_exempt
# def get_radical(request):
# 	queryset = Radical.objects.all()#[0:10]
# 	a = serialize("json", queryset,ensure_ascii=False)
# 	b = json.loads(a)
# 	c = []
# 	for item in b:
# 		c.append(item['fields'])
# d = json.dumps(c,ensure_ascii=False)
# return HttpResponse(d,content_type="application/json")
