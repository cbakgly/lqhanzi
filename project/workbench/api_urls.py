# -*- coding:utf8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from views import api_views

router = routers.DefaultRouter()
router.register(r'diaries', api_views.DiaryViewSet, base_name='diaries')
router.register(r'credits', api_views.CreditViewSet, base_name='credits')
router.register(r"redeems", api_views.RedeemViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r"credits/certain_user_credits/$", api_views.CreditViewSet.as_view({'get': 'certain_user_credits'}))
]
