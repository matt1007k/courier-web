from django.db import models

class Address(models.Model):
    address = models.CharField(max_length=150, verbose_name='dirección')
    district = models.CharField(max_length=100, verbose_name='distrito')
    city = models.CharField(max_length=150, verbose_name='ciudad')
    references = models.TextField(max_length=200, verbose_name='referencia')