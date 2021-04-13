import string
import random
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='código')
    discount = models.FloatField(default=0.0, verbose_name='descuento')
    valid_from = models.DateTimeField(verbose_name='fecha de inicio')
    valid_to = models.DateTimeField(verbose_name='fecha de vencimiento')
    used = models.BooleanField(default=False, verbose_name='usado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='fecha de creación')

    def __str__(self) -> str:
        return self.code

    def use(self):
        self.used = True
        self.save()

    class Meta:
        verbose_name = 'código promocional'
        verbose_name_plural = 'código promocionales'

@receiver(pre_save, sender=PromoCode)
def set_code(sender, instance, *args, **kwargs):
    if instance.code:
        return

    chars = string.ascii_uppercase + string.digits
    instance.code = ''.join( random.choice(chars) for _ in range(10) )

