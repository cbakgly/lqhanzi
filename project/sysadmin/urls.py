# -*- coding:utf8 -*-
from django.conf.urls import url
from views import task_package

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    # 工作打卡
    # url(r'task-package-management', task_package.index, name='m3.task-package-management'),
    url(r'task/$', task_package.task, name='m3.task'),
    url(r'task-package/$', task_package.task_package, name='m3.task_package'),
    url(r'check-in/$', task_package.check_in, name='m3.check-in'),
    url(r'credits/$', task_package.credits, name='m3.credits'),
    url(r'reward/$', task_package.reward, name='m3.reward'),
    url(r'forum/$', task_package.forum, name='m3.forum'),
    url(r'user-management/$', task_package.user_management, name='m3.user-management'),
    url(r'access-privilege/$', task_package.access_privilege, name='m3.access-privilege'),
    url(r'hanzi-parts/$', task_package.hanzi_parts, name='m3.hanzi-parts'),
    url(r'hanzi-radical/$', task_package.hanzi_radicals, name='m3.hanzi-radical'),
    url(r'task-type-management/$', task_package.task_type_management, name='m3.task-type-management'),
    url(r'^$', task_package.task_package)

]
