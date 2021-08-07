from django.db import models

from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import post_save

class User(AbstractUser):
    avatar = models.ImageField(upload_to="users/%Y/%m/%d/", null=False, blank=False)
    is_email_verified = models.BooleanField(default=False, verbose_name='correo verificado')

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

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def editAvatar(self, avatarFile):
        self.avatar = avatarFile
        self.save()

    def change_password(self, new_password):
        self.set_password(new_password)
        self.save()
