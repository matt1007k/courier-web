import decimal
from django.db import models

from django.db.models.signals import pre_save

from django.urls.base import reverse
from clients.models import Client
from drivers.models import Driver

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING'
        IN_PROCESS = 'IN_PROCESS'
        DELIVERED = 'DELIVERED'
        CANCELED = 'CANCELED'

    class TypeTicket(models.TextChoices):
        FACTURA = 'FACTURA'
        BOLETA = 'BOLETA'

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Motorizado')
    tracking_code = models.CharField(max_length=8, unique=True, verbose_name="Código de seguimiento")
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING, verbose_name='Estado')
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    type_ticket = models.CharField(max_length=10, choices=TypeTicket.choices, default=TypeTicket.FACTURA, verbose_name="Comprobante electrónico")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    payed_image = models.ImageField(upload_to='orders/%Y/%m/%d/', null=True, blank=True, verbose_name='imagen del pago realizado')
    igv = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    sub_total = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return self.tracking_code 

    def get_index_path(self):
        return reverse('orders:index')

    def get_detail_path(self):
        return reverse('orders:detail', kwargs={'id': self.pk})

    def get_update_path(self):
        return reverse('orders:update', kwargs={'id': self.pk})

    def get_delete_path(self):
        return reverse('orders:delete', kwargs={'id': self.pk})

    def update_totals(self):
        self.update_total()
        self.update_subtotal()

    def update_subtotal(self):
        igv = self.total * decimal.Decimal(0.18)
        self.igv = igv
        self.sub_total = self.total - igv 
        self.save()

    def update_total(self):
        self.total = sum([ detail.price_rate for detail in self.detail_set.all() ])
        self.save()

    @property
    def get_first_detail(self):
        return self.detail_set.first()

    class Meta:
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"

def set_driver(sender, instance, *args, **kwargs):
    if instance.client and instance.client.driver_code:
        driver = Driver.objects.filter(code=instance.client.driver_code).first()
        instance.driver = driver

pre_save.connect(set_driver, sender=Order)