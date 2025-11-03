from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid
from rest_framework.response import Response

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            return Response({"message": "The Username field must be set."}, status=400)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            return Response({"message": "Superuser must have is_staff=True."}, status=400)
        if extra_fields.get("is_superuser") is not True:
            return Response({"message": "Superuser must have is_superuser=True."}, status=400)

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        name = f"{self.full_name}".strip()
        return name if name else self.username

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        super().save(*args, **kwargs)