from django.urls import path
from . import views
from . import page_views
urlpatterns = [
    # rest api views
    path("user-profile/", views.UserRegister.as_view(), name="user-profile"),

    # page api views
    path("signup/", page_views.signup, name="signup"),
    path("verify_otp/", page_views.verifyopt ,name="verify_otp"),
]