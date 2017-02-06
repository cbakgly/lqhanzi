# -*- coding:utf8 -*-
from django.conf.urls import url
from views import diaries, task_package, search, forum, credits, task

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    # 工作打卡
    url(r'diaries$', diaries.index, name='m2.diaries'),

    # 积分排行榜，积分详情，我的兑换
    url(r'credits-ranking$', credits.ranking_page, name='m2.credits-ranking'),
    url(r'credits-details$', credits.details_page, name='m2.credits-details'),
    url(r'credits-redeem$', credits.redeem_page, name='m2.credits-redeem'),

    # 任务进行中，已完成，领任务，进行中之拆字、录入、去重详情
    url(r'task-package/ongoing$', task_package.task_package_ongoing, name='m2.task-package-ongoing'),
    url(r'task-package/completed$', task_package.task_package_complete, name='m2.task-package-completed'),
    url(r'task-package/new$', task_package.new_task_page, name='m2.new-task-package'),
    url(r'task-package/(?P<package_id>\d+)/split$', task_package.task_package_split_list, name='m2.task-package-split-list'),
    url(r'task-package/(?P<package_id>\d+)/input$', task_package.task_package_input_list, name='m2.task-package-input-list'),
    url(r'task-package/(?P<package_id>\d+)/dedup$', task_package.task_package_dedup_list, name='m2.task-package-dedup-list'),

    # 我的任务拆字，拆字，去重，录入
    url(r'task/split$', task.task_split, name='m2.task-split'),
    url(r'task/input$', task.task_input, name='m2.task-input'),
    url(r'task/dedup$', task.task_dedup, name='m2.task-dedup'),

    url(r'search/lq-hanzi$', search.lq_hanzi_db_search, name='m2.lq-hanzi-search'),
    url(r'search/lq-split$', search.lq_split_db_search, name='m2.lq-split-search'),
    url(r'search/cn-dict-input$', search.cn_dict_input_db_search, name='m2.cn-dict-input-search'),
    url(r'search/cn-dict-dedup$', search.cn_dict_dedup_db_search, name='m2.cn-dict-dedup-search'),
    url(r'search/korean-dedup$', search.korean_dedup_db_search, name='m2.korean-dedup-search'),
    url(r'search/korean-taiwan-dedup$', search.korean_taiwan_dedup_db_search, name='m2.korean-taiwan-dedup-search'),
    url(r'forum', forum.index, name='m2.forum'),

    url(r'^$', diaries.index, name='m2.home-page')
]
