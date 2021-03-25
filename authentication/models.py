from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to="users/%Y/%m/%d/", null=False, blank=False)