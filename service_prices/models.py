from django.db import models

class ServicePrice(models.Model):
    min = models.IntegerField(default=0, verbose_name='mínimo de kM')
    max = models.IntegerField(verbose_name='máximo de KM')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='precio')

    def __str__(self) -> str:
        return "S/.{}".format(round(self.price, 2))

    class Meta:
        verbose_name = 'precio del servicio'
        verbose_name_plural = 'precios del servicio'

# EL PRECIO DEL SERVICIO SE CALCULA ASÍ.

# DE OKM A 15KM S/10.00 
# DE 15KM A 35KM S/12.00 
# DE 35KM A MÁS S/15.00