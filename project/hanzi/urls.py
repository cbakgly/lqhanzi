# -*- coding:utf8 -*-

from django.conf.urls import url
from hanzi.views import hanzi

urlpatterns = [
    url(r'^$', hanzi.index)
]
