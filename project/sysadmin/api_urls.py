from rest_framework.routers import DefaultRouter
from sysadmin.views.api_operation import OperationViewSet
from sysadmin.views.api_user import UserViewSet
from sysadmin.views.api_diaries import DiariesViewSet

router = DefaultRouter()
router.register(r'operation', OperationViewSet)
router.register(r'user', UserViewSet)
router.register(r'diaries', DiariesViewSet)
urlpatterns = router.urls
