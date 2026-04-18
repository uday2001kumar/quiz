from django.shortcuts import render
from django.core.cache import cache
# rest_framwork
from rest_framework.views import APIView
from rest_framework import status
# local
from core.utils import success_response,error_response
# validators
from .validators import SendEmailOTPValidator,VerifyOTPValidator
# models
from .models import CustomUser

# Create your views here.
from rest_framework.views import APIView
from rest_framework import status

from core.utils import send_otp_email,get_tokens_for_user,SerializerErrorHandler


import random
import random

class SendEmailOTP(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            validator = SendEmailOTPValidator(data=request.data)

            if not validator.is_valid():
                print("Validation Errors:", validator.errors)
                return error_response(
                    message="Validation Error",
                    errors=validator.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            data = validator.validated_data
            email = data.get("email").lower().strip()
            role = data.get("role")

            user = CustomUser.objects.filter(
                email=email,
                role=role,
                is_active=True
            ).first()


            if not user:
                return error_response(
                    message="User not Found given Email",
                    errors="Invalid email or role",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            otp = str(random.randint(100000, 999999))

            cache_key = f"otp:{email}:{role}"
            cache.set(cache_key, otp, timeout=300)

            # 🔥 Verify stored value immediately
            debug_stored = cache.get(cache_key)
           

            send_otp_email(email, otp)


            return success_response(
                message="OTP sent successfully",
                data={"otp": otp},
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            print("ERROR:", str(e))
            return error_response(
                message="Something went wrong!",
                errors=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class VerifyEmailOTPView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            print("===== VERIFY OTP START =====")
            print("Request Data:", request.data)

            validator = VerifyOTPValidator(data=request.data)

            if not validator.is_valid():
                error = SerializerErrorHandler(validator.errors)
                return error_response(
                    message=error.error,
                    errors="validation error"
                )

            data = validator.validated_data
            email = data.get("email").lower().strip()
            otp = data.get("otp").strip()
            role = data.get("role")


            cache_key = f"otp:{email}:{role}"
            stored_otp = cache.get(cache_key)

            if not stored_otp:
                print("OTP NOT FOUND OR EXPIRED")
                return error_response(
                    message="OTP expired or not found",
                    errors="OTP expired",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            if str(stored_otp) != str(otp):
                print("OTP MISMATCH ❌")
                return error_response(
                    message="Invalid OTP",
                    errors="Incorrect OTP",
                    status_code=status.HTTP_400_BAD_REQUEST
                )


            user = CustomUser.objects.filter(
                email=email,
                role=role,
                is_active=True
            ).first()


            if not user:
                return error_response(
                    message="User not found",
                    errors="Invalid user",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            token = get_tokens_for_user(user)

            cache.delete(cache_key)

            return success_response(
                message="OTP verified successfully",
                data={"token": token,"email":email,"role":role},
                status_code=status.HTTP_200_OK
            )

        except Exception as e:
            print("ERROR:", str(e))
            return error_response(
                message="Something went wrong!",
                errors=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )