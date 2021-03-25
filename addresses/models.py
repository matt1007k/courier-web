from django.db import models

from clients.models import Client

class AddressManager(models.Manager):
    def create_or_update(self, client, address, district, city, reference):
        object, created = self.get_or_create(client=client, address=address)

        if not created:
            object.address = address
            object.district = district
            object.city = city
            object.reference = reference
        
        object.save()
        return object
        

class Address(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='cliente')
    address = models.CharField(max_length=150, verbose_name='dirección')
    district = models.CharField(max_length=100, verbose_name='distrito')
    city = models.CharField(max_length=150, verbose_name='ciudad')
    reference = models.TextField(max_length=200, verbose_name='referencia')
    address_gps = models.JSONField(null=True, blank=True, max_length=100, verbose_name='dirección gps')
    default = models.BooleanField(default=False)
    
    objects = AddressManager()

    def __str__(self) -> str:
        return self.address_complete()

    def address_all(self):
        return f"{self.address}, {self.district}, {self.city}, {self.reference}"

    def address_complete(self):
        return f"{self.address}, {self.district}, {self.city}"

    def address_city(self):
        return f"{self.district}, {self.city}"

    class Meta:
        verbose_name = "dirección"
        verbose_name_plural = "direcciones"