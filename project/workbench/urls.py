# -*- coding:utf8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from views import diaries, task_package, search, forum, credits, task

router = routers.DefaultRouter()
router.register(r'diaries', diaries.DiaryViewSet)
router.register(r'tags', diaries.TagViewSet)
router.register(r'credits', diaries.CreditViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 工作打卡
    url(r'diaries', diaries.index, name='m2.diaries'),

    # 积分排行榜，积分详情，我的兑换
    url(r'credits-ranking$', credits.ranking_page, name='m2.credits-ranking'),
    url(r'credits-details$', credits.details_page, name='m2.credits-details'),
    url(r'credits-redeem$', credits.redeem_page, name='m2.credits-redeem'),

    # 任务进行中，已完成，领任务，进行中之拆字、录入、去重详情
    url(r'task-package/ongoing$', task_package.task_package, name='m2.task-package-ongoing'),
    url(r'task-package/completed$', task_package.task_package, name='m2.task-package-completed'),
    url(r'task-package/new$', task_package.new_task_page, name='m2.new-task-package'),
    url(r'task-package/split/list$', task_package.task_package_split_list, name='m2.task-package-split-list'),
    url(r'task-package/input/list$', task_package.task_package_input_list, name='m2.task-package-input-list'),
    url(r'task-package/dedup/list$', task_package.task_package_dedup_list, name='m2.task-package-dedup-list'),

    # 我的任务拆字，拆字，去重，录入
    url(r'task/split$', task.task_split, name='m2.task-split'),
    url(r'task/input$', task.task_input, name='m2.task-input'),
    url(r'task/dedup$', task.task_dedup, name='m2.task-dedup'),

    url(r'search', search.index, name='m2.hanzi-lib-search'),
    url(r'forum', forum.index, name='m2.forum'),

    url(r'^$', diaries.index, name='m2.home-page')
]
