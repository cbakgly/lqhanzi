from rest_framework.routers import DefaultRouter
from sysadmin.views.api_tasks import TasksViewSet

router = DefaultRouter()
router.register(r'tasks', TasksViewSet)
urlpatterns = router.urls
