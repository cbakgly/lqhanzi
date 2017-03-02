# coding=utf-8

from django.conf.urls import url
from django.views.generic.base import RedirectView
from views import stroke, variant, dicts

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/stroke_search', permanent=False), name='m1.index'),
    url(r'^index/$', RedirectView.as_view(url='/stroke_search', permanent=False), name='m1.stroke-search'),
    url(r'^stroke_search/$', stroke.stroke_search, name='m1.stroke-search'),
    url(r'^stroke_normal_search/$', stroke.stroke_normal_search, name='m1.stroke-normal-search'),
    url(r'^stroke_advanced_search/$', stroke.stroke_advanced_search, name='m1.stroke-advanced-search'),
    url(r'^inverse_search/$', stroke.inverse_search, name='m1.inverse-search'),
    url(r'^variant_search/$', variant.variant_search, name='m1.variant-search'),
    url(r'^variant_detail/$', variant.variant_detail, name='m1.variant-detail'),
    url(r'^dicts/?$', RedirectView.as_view(url='/dicts/taiwan', permanent=False), name='m1.dicts'),
    url(r'^dicts/taiwan/$', dicts.taiwan, name="m1.dicts-taiwan"),
    url(r'^dicts/taiwan/detail/$', dicts.taiwan_detail, name="m1.dicts-taiwan-detail$"),
    url(r'^dicts/taiwan/std_hanzi/$', dicts.taiwan_std_hanzi, name="m1.dicts-taiwan-std-hanzi"),
    url(r'^dicts/korean/$', dicts.korean, name="m1.dicts-korean"),
    url(r'^dicts/korean/detail/$', dicts.korean_detail, name="m1.dicts-korean-detail$"),
    url(r'^dicts/hanyu/', dicts.hanyu, name="m1.dicts-hanyu"),
    url(r'^dicts/dunhuang/$', dicts.dunhuang, name="m1.dicts-dunhuang"),
    url(r'^dicts/dicts_search/$', dicts.dicts_search, name='m1.dicts-search'),

]
