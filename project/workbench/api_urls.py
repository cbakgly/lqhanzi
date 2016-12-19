# -*- coding:utf8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from views import diaries, task_package

router = routers.DefaultRouter()
router.register(r'diaries', diaries.DiaryViewSet)
router.register(r'tags', diaries.TagViewSet)
router.register(r'credits', diaries.CreditViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]