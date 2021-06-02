import uuid
from datetime import datetime
from django.db import models
from django.db.models.fields.related import OneToOneField

from authentication.models import User
from clients.models import Client

from django.utils.text import slugify
from django.db.models.signals import pre_save

from courier_app.utils import phone_regex

class Driver(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuario')
    first_name = models.CharField(max_length=100, verbose_name='Nombre')
    last_name = models.CharField(max_length=100, verbose_name='Apellidos')
    slug = models.SlugField(blank=True, null=True, unique=True)
    code = models.CharField(max_length=9, unique=True, verbose_name='código')
    dni = models.CharField(max_length=8, unique=True)
    cell_phone = models.CharField(validators=[phone_regex] , max_length=9, verbose_name='Num. de celular')
    cell_phone2 = models.CharField(max_length=9, null=True, blank=True, verbose_name='Num. de celular 2 (opcional)')
    address = models.CharField(max_length=100, verbose_name='dirección')
    references = models.TextField(max_length=200, verbose_name='referencias')
    district = models.CharField(max_length=100, verbose_name='distrito')
    address_gps = models.JSONField(null=True, blank=True, max_length=100, verbose_name='dirección actual')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    def __str__(self) -> str:
        return self.full_name()

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def orders_delivered_count(self):
        return self.assigndeliveryaddress_set.filter(detail__status='EN').count()

    def get_last_orders_origin_address(self, take=None):
        return self.assignoriginaddress_set.all().order_by('-created_at')[:take]

    def get_orders_origin_address(self):
        return self.assignoriginaddress_set.all()

    def get_orders_origin_address_today(self):
        return self.get_orders_origin_address().filter(created_at__gte=datetime.now().strftime('%Y-%m-%d'))
    
    def get_total_price_rate_orders_origin_address_today(self):
        return sum([assign.detail.price_rate for assign in self.get_orders_origin_address_today()])

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

class PaymentAccount(models.Model):
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, verbose_name='motorizado')
    bank = models.CharField(max_length=150, verbose_name='banco')
    account_number = models.CharField(max_length=14, verbose_name='número de cuenta')
    bank_account_number = models.CharField(max_length=20, verbose_name='número de cuenta interbancaria')
    owners = models.CharField(max_length=150, verbose_name='nombre completo del titular')
    dni = models.CharField(max_length=8, verbose_name='DNI del titular')

    def __str__(self) -> str:
        return self.owners

    class Meta:
        verbose_name = "cuenta de pago"
        verbose_name_plural = "cuentas de pago"