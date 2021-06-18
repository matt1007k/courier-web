import json
from typing import Dict
from django.db import models
from django.urls import reverse

from clients.models import Client

from courier_app.utils import phone_regex
from django.core.validators import validate_email

class AddressManager(models.Manager):
    def create_or_update(self, client, full_name, email, cell_phone, address, district, city, reference, address_gps, address_detail):
        object, created = self.get_or_create(client=client, address=address)

        if not created:
            object.full_name = full_name
            object.email = email
            object.cell_phone = cell_phone
            object.address = address
            object.district = district
            object.city = city
            object.reference = reference
            # object.address_gps = json.loads(address_gps)
            object.address_gps = address_gps
            object.address_detail = address_detail
            object.save()
        
        return object
        
    def update_or_create_address_origin(self, client, form_cleaned_data: Dict):
        address_origin = self.update_or_create(
                client = client,
                full_name = form_cleaned_data['origin_full_name'],
                email = form_cleaned_data['origin_email'],
                cell_phone = form_cleaned_data['origin_cell_phone'],
                address = form_cleaned_data['origin_address'],
                district = form_cleaned_data['origin_district'],
                city = form_cleaned_data['origin_city'],
                reference = form_cleaned_data['origin_reference'],
                address_detail = form_cleaned_data['origin_address_detail'],
                address_gps = form_cleaned_data['origin_position']
            )
        return address_origin[0]

    def update_or_create_address_destiny(self, client, form_cleaned_data):
        address_destiny = self.update_or_create(
                client = client,
                full_name = form_cleaned_data['destiny_full_name'],
                email = form_cleaned_data['destiny_email'],
                cell_phone = form_cleaned_data['destiny_cell_phone'],
                address = form_cleaned_data['destiny_address'],
                district = form_cleaned_data['destiny_district'],
                city = form_cleaned_data['destiny_city'],
                reference = form_cleaned_data['destiny_reference'],
                address_detail = form_cleaned_data['destiny_address_detail'],
                address_gps = form_cleaned_data['destiny_position']
            )
        return address_destiny[0]
        

class Address(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='cliente')
    full_name = models.CharField(max_length=100, verbose_name='nombre completo')
    email = models.CharField(validators=[validate_email],max_length=150, null=True, blank=True, verbose_name='correo electrónico (opcional)')
    cell_phone = models.CharField(validators=[phone_regex],max_length=9, verbose_name='num. de celular')
    address = models.CharField(max_length=150, verbose_name='dirección')
    district = models.CharField(max_length=100, verbose_name='distrito')
    city = models.CharField(max_length=150, verbose_name='ciudad o País')
    reference = models.TextField(max_length=200, verbose_name='referencia')
    address_detail = models.CharField(max_length=200, verbose_name='N° de puerta/Lte/Mz/Dpto/Piso')
    address_gps = models.JSONField(null=True, blank=True, max_length=100, verbose_name='dirección gps')
    default = models.BooleanField(default=False, verbose_name='Principal')
    
    objects = AddressManager()

    def __str__(self) -> str:
        return self.address_complete()

    def get_index_path(self):
        return reverse('addresses:index')

    def get_update_path(self):
        return reverse('addresses:update', kwargs={'pk': self.pk})

    def get_delete_path(self):
        return reverse('addresses:delete', kwargs={'pk': self.pk})

    def address_all(self):
        return f"{self.address}, {self.district}, {self.city}, {self.reference}"

    def address_complete(self):
        return f"{self.address}, {self.district}, {self.city}"

    def address_district(self):
        return f"{self.address}, {self.district}"
        
    def address_city(self):
        return f"{self.district}, {self.city}"

    def update_default(self, default=False):
        self.default = default
        self.save()

    class Meta:
        verbose_name = "dirección"
        verbose_name_plural = "direcciones"