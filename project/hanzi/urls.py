#coding=utf-8

from django.conf.urls import url#, patterns
# from django.conf.urls.static import static
import views#,views2

urlpatterns = [
    url(r'^index$',views.stroke_search),#模块主页
    # url(r'^variant$',views.variant),

    # url(r'^get_parts$',views.get_parts),
    # url(r'^get_radical$',views.get_radical),   
    url(r'^stroke_search$',views.stroke_search),

    url(r'^stroke_ajax_search$',views.stroke_ajax_search),

    url(r'^variant_search$',views.variant_search),

    url(r'^variant_detail$',views.variant_detail),

    url(r'^dicts$',views.dicts),
    url(r'^dicts_search$',views.dicts_search),


    # url(r'^radical$',views2.radical),

    # url(r'^check$',views2.check),

    # url(r'^variant2$',views.variant2),
    # url(r'^iframe/',views.show_iframe),
    # url(r'^yitizi/',views.show_yitizi),

    # url(r'^CheckDictByRadical$',views2.CheckByRadical),



    # url(r'^check_by_bujian$',views.check_by_bujian),
    
    # url(r'^urA',views.show_ura),
    # url(r'^wa',views.show_wa),
    # url(r'^sa',views.show_sa),
    # url(r'^fua',views.show_fua),

    # url(r'^wa\d{1,5}.htm$',views.show_tw_wa),
    # url(r'^wa',viewsBig5.show_tw_wa),    
    # url(r'^loginpage$',views.loginpage),
    # url(r'^login$',views.login),
    # url(r'^logout$',views.logout),
	# url(r'^GetUserList/$',views.GetUserList),
	# url(r'^DleUser/$',views.DleUser),
    # url(r'^ModUser/$',views.ModUser),

]