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
