from django.db import models
from authentication.models import CustomUser
from django.utils import timezone
from datetime import timedelta


# subscription plan
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE
    )

    start_date = models.DateTimeField(default=timezone.now)

    end_date = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        # 🔥 Auto calculate end_date
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"

    class Meta:
        db_table = "user_subscriptions"