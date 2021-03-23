from django.db import models

from authentication.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
    first_name = models.CharField(max_length=100, verbose_name='Nombre') 
    last_name = models.CharField(max_length=150, verbose_name='Apellidos') 
    address = models.CharField(max_length=200, verbose_name='Dirección')
    address_gps = models.JSONField(null=True, blank=True, verbose_name='Dirección GPS')
    logo = models.ImageField(upload_to="clients/")
    store_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre de tienda')
    driver_code = models.CharField(max_length=12, verbose_name='código de motorizado')
    social_media = models.JSONField(null=True, blank=True, verbose_name='redes sociales')

    def __str__(self) -> str:
        return self.full_name()

    def full_name(self) -> str:
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
