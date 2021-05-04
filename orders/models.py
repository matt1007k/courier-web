import decimal
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.translation import gettext_lazy as _
from django.db import models

from django.db.models.signals import pre_save

from django.urls.base import reverse
from clients.models import Client
from promo_codes.models import PromoCode

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        REGISTERED = 'RE', _('Registrado')
        COMPLETED = 'CO', _('Completado')
        CANCELED = 'CA', _('Cancelado')

    class TypeTicket(models.TextChoices):
        FACTURA = 'FACTURA'
        BOLETA = 'BOLETA'

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente')
    tracking_code = models.CharField(max_length=8, unique=True, null=True, blank=True, verbose_name="Código de seguimiento")
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.REGISTERED, verbose_name='Estado')
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    type_ticket = models.CharField(max_length=10, choices=TypeTicket.choices, default=TypeTicket.FACTURA, verbose_name="Comprobante electrónico")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    payed_image = models.ImageField(upload_to='orders/%Y/%m/%d/', null=True, blank=True, verbose_name='imagen del pago realizado')
    igv = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    sub_total = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    promo_code = models.OneToOneField(PromoCode, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.tracking_code)

    def get_index_path(self):
        return reverse('orders:index')

    def get_detail_path(self):
        return reverse('orders:detail', kwargs={'pk': self.pk})

    def get_update_path(self):
        return reverse('orders:update', kwargs={'pk': self.pk})

    def get_delete_path(self):
        return reverse('orders:delete', kwargs={'pk': self.pk})

    def apply_promo_code(self, promo_code):
        if self.promo_code is None:
            self.promo_code = promo_code
            self.save()

            self.update_totals()
            promo_code.use()

    def get_discount(self):
        if self.promo_code:
            discount = (self.get_total() * decimal.Decimal((self.promo_code.discount / 100))) 
            return round(float(discount), 2)

        return 0

    def get_total_previous(self):
        return self.total + decimal.Decimal(self.get_discount())

    def update_totals(self):
        self.update_total()
        self.update_subtotal()

    def update_subtotal(self):
        igv = self.total * decimal.Decimal(0.18)
        self.igv = igv
        self.sub_total = self.total - igv 
        self.save()

    def update_total(self):
        self.total = self.get_total() - decimal.Decimal(self.get_discount())
        self.save()

    def get_total(self):
        return sum([ detail.price_rate for detail in self.detail_set.all() ])

    def payed_order(self, payed_image, tracking_code, type_ticket):
        self.payed_image = payed_image
        self.tracking_code = tracking_code        
        self.type_ticket = type_ticket
        self.save()

    def canceled(self):
        self.status = Order.OrderStatus.CANCELED
        self.save()

    def completed(self):
        self.status = Order.OrderStatus.COMPLETED
        self.save()

    def get_tracking_code_text(self):
        return '# TRACKING {}'.format(self.tracking_code)
    
    def created_at_naturaltime(self):
        return naturaltime(self.created_at)
    
    @property
    def get_first_detail(self):
        return self.detail_set.first()

    class Meta:
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"


# def set_driver(sender, instance, *args, **kwargs):
#     if instance.client and instance.client.driver_code:
#         driver = Driver.objects.filter(code=instance.client.driver_code).first()
#         instance.driver = driver

# pre_save.connect(set_driver, sender=Order)