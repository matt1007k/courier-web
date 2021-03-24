from django.db import models

from clients.models import Client

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
    tracking_code = models.CharField(max_length=8, unique=True, verbose_name="Código de seguimiento")
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING, verbose_name='Estado')
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    type_ticket = models.CharField(max_length=10, choices=TypeTicket.choices, default=TypeTicket.FACTURA, verbose_name="Comprobante electrónico")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __str__(self) -> str:
        return self.tracking_code 

    class Meta:
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"