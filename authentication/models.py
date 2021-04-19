from django.db import models

from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import post_save

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
    
    def set_driver(self):
        driver_group = Group.objects.get(name='Motorizado')
        self.groups.add(driver_group)

    def set_client(self):
        client_group = Group.objects.get(name='Cliente')
        self.groups.add(client_group)
