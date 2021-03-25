from orders.models import Order
from django.db import models
from addresses.models import Address

class Detail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='pedido')
    first_name = models.CharField(max_length=100, verbose_name='nombre')
    last_name = models.CharField(max_length=100, verbose_name='apellidos')
    email = models.CharField(max_length=150, verbose_name='correo electrónico')
    cell_phone = models.CharField(max_length=9, verbose_name='num. de celular')
    image = models.ImageField(upload_to="details-order/%Y/%m/%d/", null=True, blank=True, verbose_name='imagen del paquete')
    description = models.TextField(max_length=150, null=True, blank=True, verbose_name='descripción del paquete')
    address_origin = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_origin', verbose_name='dirección de recojo')
    address_destiny = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_destiny',verbose_name='dirección de destino')
    distance = models.DecimalField(max_digits=10, decimal_places=1, verbose_name='distancia', default=0)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio de tarifa', default=0)

    def __str__(self) -> str:
        return self.full_name()

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = "detalle"
        verbose_name_plural = "detalles"