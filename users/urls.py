from django.urls import path
from . import views
urlpatterns = [
    # rest api views
    path("user-profile/", views.UserRegister.as_view(), name="user-profile"),
]