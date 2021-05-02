import decimal
from typing import Dict
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from orders.models import Order
from django.db import models
from addresses.models import Address

from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

class Detail(models.Model):
    class PackageStatus(models.TextChoices):
        PENDING = 'PE', _('Pendiente')
        RECEIVED = 'RE', _('Recibido')
        WAREHOUSE = 'AL', _('En Almacén')
        DELIVERED = 'EN', _('Entregado')

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='pedido')
    size = models.CharField(max_length=150, verbose_name='tamaño')
    contain = models.CharField(max_length=100, verbose_name='¿Qué contiene?')
    value = models.CharField(max_length=150, verbose_name='valor del paquete')
    image = models.ImageField(upload_to="details-order/%Y/%m/%d/", null=True, blank=True, verbose_name='imagen del paquete')
    description = models.TextField(max_length=200, null=True, blank=True, verbose_name='nota')
    address_origin = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_origin', verbose_name='dirección de recojo')
    address_destiny = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_destiny',verbose_name='dirección de destino')
    distance = models.DecimalField(max_digits=10, decimal_places=1, verbose_name='distancia', default=0)
    price_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio de tarifa', default=0)
    status = models.CharField(max_length=50, choices=PackageStatus.choices, default=PackageStatus.PENDING)

    def __str__(self) -> str:
        return self.full_name()

    def full_name(self):
        return "%s %s" % (self.order.tracking_code, self.contain)

    def origin_map_path(self):
        return reverse('details:origin-map', kwargs={'pk': self.pk})

    def destiny_map_path(self):
        return reverse('details:destiny-map', kwargs={'pk': self.pk})

    def update_addressess(self, client, origin_form, destiny_form):
        self.address_origin = self.update_or_create_address_origin(client=client, form_cleaned_data=origin_form)
        self.address_destiny = self.update_or_create_address_destiny(client=client, form_cleaned_data=destiny_form)
        self.save()

    def update_information(self, order, instance, distance, price_rate):
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

    def is_received(self):
        self.status = Detail.PackageStatus.RECEIVED
        self.save()

    def is_(self):
        self.status = Detail.PackageStatus.RECEIVED
        self.save()

    class Meta:
        verbose_name = "detalle"
        verbose_name_plural = "detalles"

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