
from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import SubscriptionPlanViewSet

router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet, basename='plans')

urlpatterns = [
    # rest api
    path("", include(router.urls)),
]