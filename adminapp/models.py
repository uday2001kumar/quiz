from django.db import models
from authentication.models import CustomUser,BaseModel
from django.utils import timezone
from datetime import timedelta


# subscription plan
class SubscriptionPlan(BaseModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserSubscription(BaseModel):
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



class Category(BaseModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category/', null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class SubCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='subcategory/', null=True, blank=True)

    def __str__(self):
        return self.name
    

class SubTopic(BaseModel):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="subtopics")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='subtopic/', null=True, blank=True)

    def __str__(self):
        return self.name
    


from datetime import timedelta

class Task(BaseModel):
    subtopic = models.ForeignKey(
        SubTopic,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to='task/', null=True, blank=True)

    total_questions = models.IntegerField(default=50)

    # Timer
    duration = models.DurationField(default=timedelta(minutes=30))
    passing_marks = models.IntegerField(default=25)

    def __str__(self):
        return self.title
    


class Question(BaseModel):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question_text = models.TextField()
    image = models.ImageField(upload_to='questions/', null=True, blank=True)

    marks = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text
    

class Option(BaseModel):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options"
    )

    option_text = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='options/', null=True, blank=True)

    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text if self.option_text else "Image Option"
    

class TaskAttempt(BaseModel):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="task_attempts"
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="attempts"
    )

    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

    score = models.IntegerField(default=0)

    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.task.title}"
    

class UserAnswer(BaseModel):
    attempt = models.ForeignKey(
        TaskAttempt,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    selected_option = models.ForeignKey(
        Option,
        on_delete=models.CASCADE
    )

    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.attempt.user.email} - Q{self.question.id}"