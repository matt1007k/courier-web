import string
import random
from django.utils import timezone
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.validators import validate_integer

class PromoCodeManager(models.Manager):

    def get_valid(self, code):
        now = timezone.now()
        return self.filter(code=code).filter(valid_from__lte=now).filter(valid_to__gte=now).first()

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='código')
    discount = models.IntegerField(default=0, validators=[validate_integer], verbose_name='porcentaje de descuento')
    special = models.IntegerField(default=0, validators=[validate_integer], verbose_name='descuento especial S/')
    valid_from = models.DateTimeField(verbose_name='fecha de inicio')
    valid_to = models.DateTimeField(verbose_name='fecha de vencimiento')
    used = models.BooleanField(default=False, verbose_name='usado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='fecha de creación')

    objects = PromoCodeManager()

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

