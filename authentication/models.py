from django.db import models

from django.contrib.auth.models import AbstractUser, Group

class User(AbstractUser):
    avatar = models.ImageField(upload_to="users/%Y/%m/%d/", null=False, blank=False)

    @property
    def is_client(self):
        return self.groups.filter(name='Cliente').exists()

    @property
    def is_driver(self):
        return self.groups.filter(name='Motorizado').exists()

    @property
    def is_administrator(self):
        return self.groups.filter(name='Administrador').exists()