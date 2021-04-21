from drivers.models import Driver
from django.db import models

class DriverPayment(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='motorizado')
    count_orders = models.IntegerField(default=0, verbose_name='total de pedidos')
    total = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='total pagado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='fecha del pago')

    def __str__(self) -> str:
        return self.driver

    class Meta:
        verbose_name = 'pago del motorizado'
        verbose_name_plural = 'pagos del motorizado'

class DriverPaymentRate(models.Model):
    min = models.IntegerField(default=0, verbose_name='mínimo de pedidos')
    max = models.IntegerField(default=0, verbose_name='máximo de pedidos')
    percentage = models.IntegerField(default=0, verbose_name='porcentaje de pago')

    def __str__(self) -> str:
        return f"{self.percentage}%" 

    class Meta:
        verbose_name = 'tarifario de pago del motorizado'
        verbose_name_plural = 'tarifarios de pago del motorizado'

# TARIFARIO DE PAGOS MOTORIZADOS (EDITABLE)

# DE 1 A 50 PEDIDOS 25%
# DE 51 A 100 PEDIDOS 30% 
# DE 101 A 200 PEDIDOS 35%
# DE 201 A 400 PEDIDOS 40%
# DE 401 A MÁS PEDIDOS 50%
