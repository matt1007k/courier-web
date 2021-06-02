import uuid
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse
from pages.utils import is_valid_queryparams
from courier_app.utils import phone_regex

from authentication.models import User

class ClientQuerySet(models.QuerySet):
    def search(self, query):
        if is_valid_queryparams(query):
            filters = (Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(cell_phone__icontains=query) | Q(driver_code__icontains=query))

            return self.filter(filters)
        
        return self

class ClientManager(models.Manager):
    pass

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
    slug = models.CharField(max_length=250, null=True, blank=True, unique=True, verbose_name='Identificador')
    first_name = models.CharField(max_length=100, verbose_name='Nombre') 
    last_name = models.CharField(max_length=150, verbose_name='Apellidos') 
    cell_phone = models.CharField(validators=[phone_regex],max_length=9, null=True, blank=True, verbose_name='Núm. de celular')
    driver_code = models.CharField(max_length=12, verbose_name='código de motorizado')
    store_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre de tienda (opcional)')
    logo = models.ImageField(upload_to="clients/", null=True, blank=True, verbose_name='logo de la tienda (opcional)')
    social_media = models.JSONField(null=True, blank=True, verbose_name='redes sociales')

    objects = ClientManager.from_queryset(ClientQuerySet)()

    def __str__(self) -> str:
        return self.full_name()

    def full_name(self) -> str:
        return "{} {}".format(self.first_name, self.last_name)

    def get_last_addresses(self, take=5):
        return self.address_set.all().order_by('-id')[:take] 

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    @property
    def address_default(self):
        return self.address_set.filter(default=True).first()

    @property
    def orders_count(self):
        return self.order_set.count()

    @property
    def addressess_count(self):
        return self.address_set.count()

    def has_address_default(self):
        return self.address_default is not None

    def get_index_path(self):
        return reverse('clients:index')

    def get_detail_path(self):
        return reverse('clients:detail', kwargs={'slug': self.slug})

    def get_update_path(self):
        return reverse('clients:update', kwargs={'slug': self.slug})

    def get_delete_path(self):
        return reverse('clients:delete', kwargs={'slug': self.slug})


def set_slug(sender, instance, *args, **kwargs):
    full_name = instance.full_name()
    if full_name and not instance.slug:
        slug = slugify(full_name)
        while Client.objects.filter(slug=slug).exists():
            slug = slugify(
                "%s-%s" % (full_name, str(uuid.uuid4())[:8])
            )
        instance.slug = slug

pre_save.connect(set_slug, sender=Client)