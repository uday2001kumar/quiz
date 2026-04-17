
from rest_framework.routers import DefaultRouter
from .views import SubscriptionPlanViewSet

router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet, basename='plans')

urlpatterns = router.urls