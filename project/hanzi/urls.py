# -*- coding:utf8 -*-

from django.conf.urls import url, include
from hanzi.views import hanzi

urlpatterns = [
    url(r'^$', hanzi.index)
]
