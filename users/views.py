# django
from django.shortcuts import render
from django.db import transaction

# restframework
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ValidationError

# local
from core.utils import success_response,error_response,generate_username

# validators
from .validators import UserProfileValidator

# models
from authentication.models import CustomUser
from .models import UserProfile
# Create your views here.




class UserRegister(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            print("Data:", request.data)

            validator = UserProfileValidator(data=request.data)
            validator.is_valid(raise_exception=True)
            validated_data = validator.validated_data

            full_name = validated_data.get("full_name")
            email = validated_data.get("email")
            mobile = validated_data.get("mobile")
            dob = validated_data.get("dob")

            username = generate_username(email)

            # 🔥 START TRANSACTION
            with transaction.atomic():
                try:
                    # Check duplicate email
                    if CustomUser.objects.filter(email=email).exists():
                        # Force rollback
                        transaction.set_rollback(True)
                        return error_response(
                            message="Email already exists",
                            errors="Email already exists",
                            status_code=status.HTTP_400_BAD_REQUEST
                        )

                    #  Create user
                    user = CustomUser.objects.create(
                        full_name=full_name,
                        email=email,
                        username=username,
                        mobile=mobile
                    )

                    #  Get/Create profile safely
                    profile, created = UserProfile.objects.get_or_create(user=user)


                    profile.dob = dob
                    profile.save()

                except Exception as inner_error:
                    # 🔥 Any exception → rollback
                    transaction.set_rollback(True)
                    raise inner_error

            # If everything successful → commit happens automatically
            return success_response(
                message="User registered successfully!",
                data={
                    "user_id": user.id,
                    "email": user.email
                },
                status_code=status.HTTP_201_CREATED
            )

        except ValidationError as e:
            return error_response(
                message="Validation failed",
                errors=e.detail,
                status_code=400
            )

        except Exception as e:
            return error_response(
                message="Something went wrong!",
                errors=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )