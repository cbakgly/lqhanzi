from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from sysadmin.views.api_operation import OperationViewSet
from sysadmin.views.api_user import UserViewSet
from sysadmin.views.api_tasks import TasksViewSet
from sysadmin.views.api_task_packages import TaskPackagesViewSet

router = DefaultRouter()
router.register(r'task_packages', TaskPackagesViewSet)
urlpatterns = router.urls
