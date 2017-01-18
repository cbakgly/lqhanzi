#coding=utf-8

# Create your views here.
# User/views.py
from django.core.serializers import serialize
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.db.models import Q
from django.forms.models import model_to_dict
import json
from hanzi.models import HanziSet,Radical

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#本项目中用到了paginator分页模块
#安装方式  sudo pip install paginator




#第一个参数是所属字典，第二个是图片id
#返回值：图片在静态文件中的路径，以static开头
def get_pic_path(char_dict,pic_id):
	try:
		obj = HanziSet.objects.get( Q(source=char_dict ) & Q(hanzi_pic_id=pic_id) ) 

		path = ''
		if (char_dict == '2') :  			 	#如果是台湾图片
			forst_two_letter = pic_id[0:2]		#截取前两个字母
			path = '/static/tw/' + forst_two_letter + '/' + pic_id + '.png'
		elif (char_dict == '3'):					#如果是汉语大字典里的字
			path = '/static/hy/' + pic_id + '.png'
			print path
		elif (char_dict == '4') :   				#如果是高丽字典里的字
			if(obj.variant_type == 0):			#如果是正字
				path = '/static/gl/standard/' + pic_id + '.png'
			else:
				path = '/static/gl/variant/' + pic_id + '.png'
		elif (char_dict == '5'):		#如果是敦煌俗字典里的字
			path = '/static/dh/' + pic_id + '.png'
		else:
			pass
		return path		
	except:
		return ''






# @csrf_exempt
# def CheckByRadical(request):
# 	radical = request.POST['radical']
# 	result = HanziSet.objects.filter( Q(radical__exact=radical) ).order_by('source')
# 	a = serialize("json", result,ensure_ascii=False)
# 	b = json.loads(a)
# 	c = []
# 	for item in b:
# 		c.append(item['fields'])
# 	for item in c:
# 		if(item['hanzi_pic_id'] != ""):
# 			item['pic_url'] = get_pic_path( str(item['source']),item['hanzi_pic_id'] )
# 	d = json.dumps(c,ensure_ascii=False)
# 	return HttpResponse(d,content_type="application/json")


@csrf_exempt
def check(request):
	radical = request.GET['radical']
	page = request.GET.get('page') # 获取页码

	# pagenum = int(page)

	hanzi_list = HanziSet.objects.filter( Q(radical__exact=radical) ).order_by('source')

	# for i in range(10):
	# 	print type(hanzi_list[(pagenum-1)*10+i].hanzi_pic_id)	
	# 	print hanzi_list[(pagenum-1)*10+i].hanzi_pic_id
	# 	if( hanzi_list[(pagenum-1)*10+i].hanzi_pic_id != ""):
	# 		hanzi_list[(pagenum-1)*10+i].pic_url = get_pic_path( str(hanzi_list[(pagenum-1)*10+i].source),hanzi_list[(pagenum-1)*10+i].hanzi_pic_id.encode("utf-8") )
			# print hanzi_list[(pagenum-1)*10+i].pic_url

	paginator = Paginator(hanzi_list, 10)  # 实例化一个分页对象

	try:
		result = paginator.page(page)  # 获取某页对应的记录
	except PageNotAnInteger:  # 如果页码不是个整数
		result = paginator.page(1)  # 取第一页的记录
	except EmptyPage:  # 如果页码太大，没有相应的记录
		result = paginator.page(paginator.num_pages)  # 取最后一页的记录

	# return render_to_response('checkresult.htm', {'result': result})
	return render(request, 'checkresult.htm', {'result': result,'radical':radical} )
	# return render(request, 'iframe.htm', context) 



'''
这个函数，里边的分页功能将由我自己写，不用Paginator
'''
@csrf_exempt
def check_by_bujian(request):
	page = 0
	limit = 50
	if request.method == 'GET':
		terms = request.GET['terms']
		page  = int(request.GET['page']) # 获取页码
	elif request.method == 'POST':
		terms = request.POST['terms']
		page  = int(request.POST['page']) # 获取页码

	pages = HanziSet.objects.filter( Q(mix_split__contains=terms)  ).count() / limit + 1
	result = HanziSet.objects.filter( Q(mix_split__contains=terms)  ).order_by('source')[(page-1)*limit:page*limit]
	for item in result:
		if( item.hanzi_pic_id != "" ):
			item.pic_url = get_pic_path( str(item.source),item.hanzi_pic_id ) 

	context = {}
	context['page'] = page
	context['pages'] = pages
	context['terms'] = terms
	context['result'] = result
	return render(request, 'checkresult2.htm', context) 



