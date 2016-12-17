# -*- coding:utf8 -*-
from django.conf.urls import url, include
from views import diaries, task


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'task', task.index)
]