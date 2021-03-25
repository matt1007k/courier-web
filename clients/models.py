from django.db import models

from authentication.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
    first_name = models.CharField(max_length=100, verbose_name='Nombre') 
    last_name = models.CharField(max_length=150, verbose_name='Apellidos') 
    cell_phone = models.CharField(max_length=9, null=True, blank=True, verbose_name='Núm. de celular')
    driver_code = models.CharField(max_length=12, verbose_name='código de motorizado')
    store_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre de tienda')
    logo = models.ImageField(upload_to="clients/", null=True, blank=True, verbose_name='logo de la tienda')
    social_media = models.JSONField(null=True, blank=True, verbose_name='redes sociales')

    def __str__(self) -> str:
        return self.full_name()

    def full_name(self) -> str:
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
