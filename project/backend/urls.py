from rest_framework.routers import SimpleRouter
from backend.views.api_diaries import DiariesViewSet
from backend.views.api_user import UserViewSet
from backend.views.api_operation import OperationViewSet
from backend.views.api_task_packages import TaskPackagesViewSet
from backend.views.api_tasks import TasksViewSet
from backend.views.api_redeem import RedeemViewSet
from backend.views.api_credits import CreditViewSet
from backend.views.api_variants_split import VariantsSplitViewSet
from backend.views.api_variants_input import VariantsInputViewSet, InputPageViewSet
from backend.views.api_variants_dedup import InterDictDedupViewSet
from backend.views.api_variants_korean_dedup import KoreanDedupViewSet
from backend.views.api_korean_dup_characters import KoreanTaiwanDupCharactersViewSet
from backend.views.api_hanzi_set import HanziSetViewSet
from backend.views.api_hanzi_parts import HanziPartViewSet
from backend.views.api_rewards import RewardViewSet

router = SimpleRouter()
router.register(r'operations', OperationViewSet, base_name='operations')
router.register(r'users', UserViewSet, base_name='user')
router.register(r'diaries', DiariesViewSet, base_name='diaries')
router.register(r'tasks', TasksViewSet, base_name='tasks')
router.register(r'task-packages', TaskPackagesViewSet, base_name='task-packages')
router.register(r'credits', CreditViewSet, base_name='credits')
router.register(r'redeems', RedeemViewSet, base_name='redeems')
router.register(r'splits', VariantsSplitViewSet, base_name='splits')
router.register(r'parts', HanziPartViewSet, base_name='hanzi-parts')
router.register(r'inputs', VariantsInputViewSet, base_name='inputs')
router.register(r'interdict-dedups', InterDictDedupViewSet, base_name='inter-dict-dedups')
router.register(r'korean-taiwan-dup-charaters', KoreanTaiwanDupCharactersViewSet, base_name='korean-taiwan-dup-characters')
router.register(r'korean-dedups', KoreanDedupViewSet, base_name='korean-dedups')
router.register(r'hanzi-set', HanziSetViewSet, base_name='hanzi-set')
router.register(r'inputpage', InputPageViewSet, base_name='inputpage')
router.register(r'reward', RewardViewSet, base_name='reward')
urlpatterns = router.urls
