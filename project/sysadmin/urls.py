# -*- coding:utf8 -*-
from django.conf.urls import url
from views import task_package

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    # 工作打卡
    # url(r'task-package-management', task_package.index, name='m3.task-package-management'),
    url(r'task', task_package.task, name='m3.task'),
    url(r'business', task_package.business, name='m3.business'),
    url(r'clock', task_package.clock, name='m3.clock'),
    url(r'integral', task_package.integral, name='m3.integral'),
    url(r'award', task_package.award, name='m3.award'),
    url(r'take', task_package.take, name='m3.take'),
    url(r'usertake', task_package.usertake, name='m3.usertake'),
    url(r'privelegs', task_package.privelegs, name='m3.privelegs'),
    url(r'parts', task_package.parts, name='m3.parts'),
    url(r'radical', task_package.radical, name='m3.radical'),
    url(r'type_data_dictionary', task_package.type_data_dictionary, name='m3.type_data_dictionary'),
    # url(r'^$', task_package.index, name='m3.task-package-management')

]
