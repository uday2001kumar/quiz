from django.db import models
from django.conf import settings
from authentication.models import BaseModel,CustomUser

class UserLevel(models.TextChoices):
    BEGINNER = "beginner", "Beginner"
    INTERMEDIATE = "intermediate", "Intermediate"
    ADVANCED = "advanced", "Advanced"
    EXPERT = "expert", "Expert"


class UserProfile(BaseModel):

    user = models.OneToOneField(CustomUser,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True
    )

    bio = models.TextField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)


    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    level = models.CharField(
        max_length=20,
        choices=UserLevel.choices,
        default=UserLevel.BEGINNER
    )

    rank = models.IntegerField(default=0)

    score = models.IntegerField(default=0)

    total_quizzes_taken = models.IntegerField(default=0)
    total_correct_answers = models.IntegerField(default=0)
    total_wrong_answers = models.IntegerField(default=0)

    streak_days = models.IntegerField(default=0)

    last_active = models.DateTimeField(null=True, blank=True)

    notifications_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "user_profiles"
        ordering = ["-score"]



