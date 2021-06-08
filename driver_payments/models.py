from django.db import models
from django.db.models import Q

from pages.utils import is_valid_queryparams

from drivers.models import Driver

class DriverPaymentQuerySet(models.QuerySet):
    def search_driver(self, query):
        if is_valid_queryparams(query):
            filters = (Q(driver__first_name__icontains=query) | Q(driver__last_name__icontains=query) | Q(driver__code__icontains=query))
            return self.filter(filters)

        return self

    def search_date_from(self, query_date):
        if is_valid_queryparams(query_date):
            return self.filter(created_at__gte=query_date)

        return self

    def search_date_to(self, query_date):
        if is_valid_queryparams(query_date):
            return self.filter(created_at__tl=query_date)

        return self

class DriverPaymentManager(models.Manager):
    pass

class DriverPayment(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='motorizado')
    count_orders = models.IntegerField(default=0, verbose_name='total de pedidos')
    total = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='total pagado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='fecha del pago')

    objects = DriverPaymentManager.from_queryset(DriverPaymentQuerySet)()

    def __str__(self) -> str:
        return self.driver.code

    class Meta:
        verbose_name = 'pago del motorizado'
        verbose_name_plural = 'pagos del motorizado'
