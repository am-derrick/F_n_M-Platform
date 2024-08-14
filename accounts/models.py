from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """user with full memner access"""
    is_full_member = models.BooleanField(default=False)