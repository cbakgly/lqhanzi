# coding=utf-8

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.stroke_search, name='m1.index'),  # 模块主页
    url(r'index$', views.stroke_search, name='m1.stroke-search'),  # 模块主页
    url(r'stroke_search$', views.stroke_search, name='m1.stroke-search'),
    url(r'stroke_ajax_search$', views.stroke_ajax_search, name='m1.stroke-ajax-search'),
    url(r'inverse_search$', views.inverse_search, name='m1.inverse-search'),
    url(r'variant_search$', views.variant_search, name='m1.variant-search'),
    url(r'variant_detail$', views.variant_detail, name='m1.variant-detail'),
    url(r'dicts$', views.dicts, name="m1.dicts"),
    url(r'dicts_search$', views.dicts_search, name='m1.dicts-search'),

    # url(r'^variant$',views.variant),
    # url(r'^yitizi/', views.show_yitizi),
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
