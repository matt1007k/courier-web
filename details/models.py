import decimal
from pages.utils import is_valid_queryparams
from django.contrib.humanize.templatetags.humanize import naturaltime
from typing import Dict
from django.db.models import query
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from django.db import models

from orders.models import Order
from drivers.models import Driver
from addresses.models import Address
from clients.models import Client
from authentication.models import User

from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from django.db.models import Q

class DetailQuerySet(models.QuerySet):
    def search_detail_and_client(self, query):
        if is_valid_queryparams(query):
            filters = Q(tracking_code=query) | Q(client__first_name__icontains=query) | Q(client__last_name__icontains=query) | Q(client__cell_phone__icontains=query)
            return self.filter(filters)
        return self

    def search_by_address_delivery(self, query):
        if is_valid_queryparams(query):
            filters = (Q(address_destiny__address__icontains=query) | Q(address_destiny__district__icontains=query) | Q(address_destiny__full_name__icontains=query) | Q(address_destiny__cell_phone__icontains=query))
            return self.filter(filters)
        return self

    def search_by_address_origin(self, query):
        if is_valid_queryparams(query):
            filters = (Q(address_origin__address__icontains=query) | Q(address_origin__district__icontains=query) | Q(address_origin__full_name__icontains=query) | Q(address_origin__cell_phone__icontains=query))
            return self.filter(filters)
        return self

class DetailManager(models.Manager):
    pass

class Detail(models.Model):
    class PackageStatus(models.TextChoices):
        PENDING = 'PE', _('Pendiente')
        RECEIVED = 'RE', _('Recibido')
        WAREHOUSE = 'AL', _('En Almacén')
        ON_ROUTE = 'ER', _('En Ruta')
        DELIVERED = 'EN', _('Entregado')
        UNDELIVERED = 'NEN', _('No Entregado')
        REPROGRAMMED = 'REPR', _('Reprogramado')

    class PackageSize(models.TextChoices):
        SMALL = 'SM', _('Pequeño')
        MEDIUM = 'MD', _('Mediano')
        LARGE = 'LG', _('Grande')

    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.CASCADE, verbose_name='cliente')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='pedido')
    tracking_code = models.CharField(max_length=8, unique=True, null=True, blank=True, verbose_name="Código de seguimiento")
    size = models.CharField(max_length=100, choices=PackageSize.choices, default=PackageSize.SMALL, verbose_name='tamaño')
    contain = models.CharField(max_length=100, verbose_name='¿Qué contiene?')
    value = models.CharField(max_length=150, verbose_name='valor del paquete')
    image = models.ImageField(upload_to="details-order/%Y/%m/%d/", null=True, blank=True, verbose_name='imagen del paquete (opcional)')
    description = models.TextField(max_length=200, null=True, blank=True, verbose_name='nota (opcional)')
    address_origin = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_origin', verbose_name='dirección de recojo')
    address_destiny = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_destiny',verbose_name='dirección de destino')
    distance = models.DecimalField(max_digits=10, decimal_places=1, verbose_name='distancia', default=0)
    price_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio de tarifa', default=0)
    status = models.CharField(max_length=50, choices=PackageStatus.choices, default=PackageStatus.PENDING, verbose_name='estado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    objects = DetailManager.from_queryset(DetailQuerySet)()

    def __str__(self) -> str:
        return str(self.tracking_code)

    def sumary_package(self):
        return "%s %s" % (self.tracking_code, self.contain)

    def get_detail_path(self):
        return reverse('details:detail', kwargs={'pk': self.pk})
        
    def get_change_status_path(self):
        return reverse('details:change-status', kwargs={'pk': self.pk})

    def origin_map_path(self):
        return reverse('details:origin-map', kwargs={'pk': self.pk})

    def destiny_map_path(self):
        return reverse('details:destiny-map', kwargs={'pk': self.pk})


    def update_addressess(self, client, origin_form, destiny_form):
        self.address_origin = self.update_or_create_address_origin(client=client, form_cleaned_data=origin_form)
        self.address_destiny = self.update_or_create_address_destiny(client=client, form_cleaned_data=destiny_form)
        self.save()

    def update_information(self, order, instance, distance, price_rate):
        self.client = order.client
        self.order = order
        self.size = instance.size
        self.contain = instance.contain
        self.value = instance.value
        self.description = instance.description
        self.image = instance.image
        self.distance = distance
        self.price_rate = price_rate
        self.save()

    def update_or_create_address_origin(self, client, form_cleaned_data: Dict):
        address_origin = Address.objects.update_or_create(
                client = client,
                full_name = form_cleaned_data['origin_full_name'],
                email = form_cleaned_data['origin_email'],
                cell_phone = form_cleaned_data['origin_cell_phone'],
                address = form_cleaned_data['origin_address'],
                district = form_cleaned_data['origin_district'],
                city = form_cleaned_data['origin_city'],
                reference = form_cleaned_data['origin_reference'],
                address_detail = form_cleaned_data['origin_address_detail'],
                address_gps = form_cleaned_data['origin_position']
            )
        return address_origin[0]

    def update_or_create_address_destiny(self, client, form_cleaned_data):
        address_destiny = Address.objects.update_or_create(
                client = client,
                full_name = form_cleaned_data['destiny_full_name'],
                email = form_cleaned_data['destiny_email'],
                cell_phone = form_cleaned_data['destiny_cell_phone'],
                address = form_cleaned_data['destiny_address'],
                district = form_cleaned_data['destiny_district'],
                city = form_cleaned_data['destiny_city'],
                reference = form_cleaned_data['destiny_reference'],
                address_detail = form_cleaned_data['destiny_address_detail'],
                address_gps = form_cleaned_data['destiny_position']
            )
        return address_destiny[0]

    def payed(self, tracking_code):
        self.tracking_code = tracking_code
        self.save()

    def pended(self):
        self.status = Detail.PackageStatus.PENDING
        self.save()

    def on_routed(self):
        self.status = Detail.PackageStatus.ON_ROUTE
        self.save()

    def received(self):
        self.status = Detail.PackageStatus.RECEIVED
        self.save()

    def wakehoused(self):
        self.status = Detail.PackageStatus.WAREHOUSE
        self.save()

    def delivered(self):
        self.status = Detail.PackageStatus.DELIVERED
        self.save()

    def undelivered(self):
        self.status = Detail.PackageStatus.UNDELIVERED
        self.save()

    def reprogrammed(self):
        self.status = Detail.PackageStatus.REPROGRAMMED
        self.save()

    def get_tracking_code_text(self):
        return '# TRACKING {}'.format(self.tracking_code)
    
    def created_at_naturaltime(self):
        return naturaltime(self.created_at)

    @property
    def is_delivered(self):
        return self.status == Detail.PackageStatus.DELIVERED

    @property
    def is_assign_origin(self):
        return AssignOriginAddress.objects.filter(detail=self).exists() 

    @property
    def is_assign_delivery(self):
        return AssignDeliveryAddress.objects.filter(detail=self).exists() 

    @property
    def is_unassign_origin(self):
        return UnassignOriginAddress.objects.filter(detail=self).exists() 

    @property
    def is_unassign_delivery(self):
        return UnassignDeliveryAddress.objects.filter(detail=self).exists() 

    class Meta:
        verbose_name = "detalle"
        verbose_name_plural = "detalles"

class AssignOriginAddress(models.Model):
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE, verbose_name='detalles del paquete')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='motorizado')
    admin = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='administrador')

    def __str__(self) -> str:
        return self.detail.tracking_code

    def update_driver(self, driver, admin):
        self.driver = driver
        self.admin = admin
        self.save()

    class Meta:
        verbose_name = 'asignar dirección de entrega'
        verbose_name_plural = 'direcciones de entrega asignadas'

class AssignDeliveryAddress(models.Model):
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE, verbose_name='detalles del paquete')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='motorizado')
    admin = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='administrador')

    def __str__(self) -> str:
        return self.detail.tracking_code

    
    def update_driver(self, driver, admin):
        self.driver = driver
        self.admin = admin
        self.save()

    class Meta:
        verbose_name = 'asignar dirección de envío'
        verbose_name_plural = 'direcciones de envío asignadas'

class UnassignOriginAddress(models.Model):
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE, verbose_name='detalles del packete')
        
    def __str__(self) -> str:
        return str(self.detail.tracking_code)

    class Meta:
        verbose_name = 'sin asignar dirección de recojo'
        verbose_name_plural = 'direcciones de recojo sin asignar'

class UnassignDeliveryAddress(models.Model):
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE, verbose_name='detalles del packete')
        
    def __str__(self) -> str:
        return str(self.detail.tracking_code)

    class Meta:
        verbose_name = 'sin asignar dirección de envío'
        verbose_name_plural = 'direcciones de envío sin asignar '

class PackageDelivered(models.Model):
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE, verbose_name='dirección de envío')
    driver = models.ForeignKey(Driver, null=True, blank=True, on_delete=models.CASCADE, verbose_name='motorizado')
    image = models.ImageField(upload_to='orders/delivered/%Y/%m/%d/', verbose_name='imagen o foto 1')
    image2 = models.ImageField(upload_to='orders/delivered/%Y/%m/%d/', verbose_name='imagen o foto 2')
    description = models.TextField(max_length=250, null=True, blank=True, verbose_name='nota (opcional)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de entrega')

    def __str__(self) -> str:
        return self.detail.address_destiny.full_name

    class Meta:
        verbose_name = 'entrega de paquete'
        verbose_name_plural = 'entrega de paquetes'

def set_price_rate(sender, instance, *args, **kargs):
    pass
    # if instance.address_origin and instance.address_destiny:
    #     distance = 1
    #     instance.distance = distance
    #     if distance > 0 and distance < 15:
    #         price = 10
    #     else:
    #         price = 0
    #     instance.price_rate = decimal.Decimal(price)


@receiver(post_save, sender=Detail)
def set_update_totals(sender, instance, *args, **kwargs):
    instance.order.update_totals()

@receiver(post_delete, sender=Detail)
def set_update_totals_after_delete(sender, instance, *args, **kwargs):
    instance.order.update_totals()

pre_save.connect(set_price_rate, sender=Detail)
# post_save.connect(set_update_totals, sender=Detail)