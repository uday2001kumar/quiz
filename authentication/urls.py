from django.urls import path
from . import views
urlpatterns = [
    path("send-email-otp/", views.SendEmailOTP.as_view(), name="admin-loginview"),
    path("veriy-email-otp/", views.VerifyEmailOTPView.as_view(), name="veriy-email-otp")
]