
from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import SubscriptionPlanViewSet
from . import page_view

router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet, basename='plans')

urlpatterns = [
    # rest api
    path("", include(router.urls)),

    # normal api
    path("dashboard/", page_view.AdminDashboardView.as_view(), name="admin-dashboard"),
    path("subscriptions/", page_view.SubscriptionPageView.as_view(), name="subscriptions"),
]