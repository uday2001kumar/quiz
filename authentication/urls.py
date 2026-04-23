from django.urls import path
from . import views

urlpatterns = [
    # rest apis
    path("send-email-otp/", views.SendEmailOTP.as_view(), name="admin-loginview"),
    path("verify-email-otp/", views.VerifyEmailOTPView.as_view(), name="verify-email-otp"),
]