from clients.models import Client
import uuid
from django.db import models
from django.db.models.fields.related import OneToOneField

from authentication.models import User

from django.utils.text import slugify
from django.db.models.signals import pre_save

class Driver(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuario')
    first_name = models.CharField(max_length=100, verbose_name='Nombre')
    last_name = models.CharField(max_length=100, verbose_name='Apellidos')
    slug = models.SlugField(blank=True, null=True, unique=True)
    code = models.CharField(max_length=9, unique=True, verbose_name='código')
    dni = models.CharField(max_length=8, unique=True)
    cell_phone = models.CharField(max_length=9, verbose_name='Num. de celular')
    cell_phone2 = models.CharField(max_length=9, null=True, blank=True, verbose_name='Num. de celular 2')
    address = models.CharField(max_length=100, verbose_name='dirección')
    references = models.TextField(max_length=200, verbose_name='referencias')
    district = models.CharField(max_length=100, verbose_name='distrito')
    address_gps = models.JSONField(null=True, blank=True, max_length=100, verbose_name='dirección actual')
    payment_account = models.CharField(max_length=14, verbose_name='número de cuenta')

    def __str__(self) -> str:
        return self.full_name()

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def orders_count(self):
        return self.order_set.count()

    def get_clients(self):
        return Client.objects.filter(driver_code=self.code)

    def get_last_clients(self, take=6):
        return self.get_clients()[:take]
    
    def get_valorations(self):
        return self.valoration_set.all().order_by('-id')

    def get_last_valorations(self, take=5):
        return self.get_valorations()[:take]
        
    def clients_count(self):
        return self.get_clients().count()

    def clients_more_count(self):
        return self.clients_count() - self.get_last_clients().count()

    def valorations_count(self):
        return self.valoration_set.count()
    
    class Meta:
        verbose_name = "motorizado"
        verbose_name_plural = "motorizados"

def set_slug(sender, instance, *args, **kargs):
    full_name = instance.full_name()
    if full_name and not instance.slug:
        slug = slugify(full_name)

        while Driver.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(full_name, str(uuid.uuid4())[:8])
            )
        instance.slug = slug

pre_save.connect(set_slug, sender=Driver)


class Vehicle(models.Model):
    driver = OneToOneField(Driver, on_delete=models.CASCADE, verbose_name='motorizado')
    serial_number = models.CharField(max_length=10, verbose_name='número de serie de la moto')
    license_code = models.CharField(max_length=10, verbose_name='código de brevete')
    license_plate_number = models.CharField(max_length=10, verbose_name='número de placa')

    def __str__(self):
        return self.serial_number

    class Meta:
        verbose_name = "vehiculo"
        verbose_name_plural = "vehiculos"