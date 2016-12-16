from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from sysadmin.views.api_sysadmin import OperationViewSet

router = DefaultRouter()
router.register(r'^operation', OperationViewSet)
urlpatterns = router.urls
