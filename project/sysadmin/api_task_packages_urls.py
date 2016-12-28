from rest_framework.routers import DefaultRouter
from sysadmin.views.api_task_packages import TaskPackagesViewSet

router = DefaultRouter()
router.register(r'task_packages', TaskPackagesViewSet)
urlpatterns = router.urls
