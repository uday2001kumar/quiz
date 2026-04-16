from rest_framework import serializers
from datetime import date

class UserProfileValidator(serializers.Serializer):

    full_name = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "required": "Full Name is required!",
            "blank": "Full Name cannot be blank"
        }
    )

    email = serializers.EmailField(
        required=True,
        allow_null=False,
        allow_blank=False,
        error_messages={
            "required": "Email is required!",
            "null": "Email field cannot be null",
            "blank": "Email field cannot be blank"
        }
    )

    username = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True,
        allow_blank=True
    )

    mobile = serializers.CharField(
        max_length=15,
        required=False,
        allow_null=True,
        allow_blank=True
    )

    bio = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )

    city = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True,
        allow_blank=True
    )

    country = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True,
        allow_blank=True
    )

    avatar = serializers.ImageField(
        required=False,
        allow_null=True
    )

    level = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )

    rank = serializers.IntegerField(
        required=False,
        default=0
    )

    total_quizzes_taken = serializers.IntegerField(
        required=False,
        default=0
    )

    streak_days = serializers.IntegerField(
        required=False,
        default=0
    )

    notifications_enabled = serializers.BooleanField(
        required=False,
        default=True
    )

    dob = serializers.DateField(required=False, allow_null=True)

    def validate_dob(self, value):

        if value and value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future!")

        return value