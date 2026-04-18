from django.urls import path
from . import views
from . import page_view
urlpatterns = [
    # rest apis
    path("send-email-otp/", views.SendEmailOTP.as_view(), name="admin-loginview"),
    path("verify-email-otp/", views.VerifyEmailOTPView.as_view(), name="verify-email-otp"),

    # django apis
    path("admin-login/",page_view.adminlogin,name="admin-login"),
]