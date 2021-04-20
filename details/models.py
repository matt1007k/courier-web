import decimal
from typing import Dict

from orders.models import Order
from django.db import models
from addresses.models import Address

from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

class Detail(models.Model):
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

    def __str__(self) -> str:
        return self.full_name()

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def update_addressess(self, client, origin_form, destiny_form):
        self.address_origin = self.update_or_create_address_origin(client=client, form_cleaned_data=origin_form)
        self.address_destiny = self.update_or_create_address_destiny(client=client, form_cleaned_data=destiny_form)
        self.save()

    def update_information(self, order, instance):
        self.order = order
        self.first_name = instance.first_name
        self.last_name = instance.last_name
        self.email = instance.email
        self.cell_phone = instance.cell_phone
        self.description = instance.description
        self.image = instance.image
        self.save()

    def update_or_create_address_origin(self, client, form_cleaned_data: Dict):
        address_origin = Address.objects.update_or_create(
                client = client,
                address = form_cleaned_data['origin_address'],
                district = form_cleaned_data['origin_district'],
                city = form_cleaned_data['origin_city'],
                reference = form_cleaned_data['origin_reference'],
            )
        return address_origin[0]

    def update_or_create_address_destiny(self, client, form_cleaned_data):
        address_destiny = Address.objects.update_or_create(
                client = client,
                address = form_cleaned_data['destiny_address'],
                district = form_cleaned_data['destiny_district'],
                city = form_cleaned_data['destiny_city'],
                reference = form_cleaned_data['destiny_reference'],
            )
        return address_destiny[0]

    class Meta:
        verbose_name = "detalle"
        verbose_name_plural = "detalles"

def set_price_rate(sender, instance, *args, **kargs):
    if instance.address_origin and instance.address_destiny:
        distance = 1
        instance.distance = distance
        if distance > 0 and distance < 15:
            price = 10
        else:
            price = 0
        instance.price_rate = decimal.Decimal(price)


@receiver(post_save, sender=Detail)
def set_update_totals(sender, instance, *args, **kwargs):
    instance.order.update_totals()

@receiver(post_delete, sender=Detail)
def set_update_totals_after_delete(sender, instance, *args, **kwargs):
    instance.order.update_totals()

pre_save.connect(set_price_rate, sender=Detail)
# post_save.connect(set_update_totals, sender=Detail)