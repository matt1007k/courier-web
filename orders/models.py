from django.db import models

from clients.models import Client

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING'
        IN_PROCESS = 'IN_PROCESS'
        DELIVERED = 'DELIVERED'
        CANCELED = 'CANCELED'
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente')
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING, verbose_name='Estado')
    shipping_total = models.DecimalField(default=10, max_digits=8, decimal_places=2, verbose_name='Precio de envio')
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __str__(self) -> str:
        return ""

    class Meta:
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"