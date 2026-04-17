from rest_framework import serializers

from rest_framework import serializers

class SendEmailOTPValidator(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        error_messages={
            "required": "Email is required",
            "blank": "Email cannot be empty",
            "invalid": "Enter a valid email address"
        }
    )

    role = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "required": "Role is required",
            "blank": "Role cannot be empty"
        }
    )

    

class VerifyOTPValidator(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        error_messages={
            "required": "Email is required",
            "blank": "Email cannot be empty",
            "invalid": "Enter a valid email address"
        }
    )

    role = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "required": "Role is required",
            "blank": "Role cannot be empty"
        }
    )


    otp = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=6,
        min_length=6,
        error_messages={
            "required": "OTP is required",
            "blank": "OTP cannot be empty",
            "max_length": "OTP must be 6 digits",
            "min_length": "OTP must be 6 digits"
        }
    )

    
