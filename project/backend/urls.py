from rest_framework.routers import SimpleRouter

from backend.views.api_diaries import DiariesViewSet
from backend.views.api_user import UserViewSet
from backend.views.api_operation import OperationViewSet
from backend.views.api_task_packages import TaskPackagesViewSet
from backend.views.api_tasks import TasksViewSet
from backend.views.api_diaries import DiaryViewSet
from backend.views.api_redeem import RedeemViewSet
from backend.views.api_credits import CreditViewSet
from backend.views.api_variants_split import VariantsSplitViewSet

router = SimpleRouter()
router.register(r'operations', OperationViewSet, base_name='operations')
router.register(r'users', UserViewSet, base_name='user')
router.register(r'diaries', DiariesViewSet, base_name='diaries')
router.register(r'tasks', TasksViewSet, base_name='tasks')
router.register(r'task-packages', TaskPackagesViewSet, base_name='task-packages')
router.register(r'diaries', DiaryViewSet, base_name='diaries')
router.register(r'credits', CreditViewSet, base_name='credits')
router.register(r"redeems", RedeemViewSet, base_name='redeems')
router.register(r"splits", VariantsSplitViewSet)
urlpatterns = router.urls
