from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
import uuid
from django.db.models import UniqueConstraint

# =======================
# BASE MODEL
# =======================
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def last_updated(self):
        return self.modified_at.astimezone()

    def created_time(self):
        return self.created_at.astimezone()


# =======================
# CHOICES
# =======================
class UserRoles(models.TextChoices):
    USER = 'user', _('User')
    ADMIN = 'admin', _('Admin')
    SUPER_ADMIN = 'superadmin', _('Super Admin')


class StatusChoices(models.TextChoices):
    ACTIVE = 'active', _('Active')
    INACTIVE = 'in_active', _('In Active')


# =======================
# MANAGER
# =======================
class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):

        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        extra_fields.setdefault("role", UserRoles.USER)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", True)

        user = self.model(username=username, email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_admin(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("role", UserRoles.ADMIN)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("role", UserRoles.SUPER_ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(username, email, password, **extra_fields)


# =======================
# CUSTOM USER
# =======================
class CustomUser(AbstractBaseUser):

    full_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE
    )

    role = models.CharField(
        max_length=25,
        choices=UserRoles.choices,
        default=UserRoles.USER
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name', 'mobile']

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        constraints = [
            UniqueConstraint(fields=['email', 'role'], name='unique_email_role'),
        ]

    def __str__(self):
        return self.email or self.username or str(self.id)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def last_updated_formatted(self):
        return self.modified_at.strftime("%d %b %y %I:%M %p")