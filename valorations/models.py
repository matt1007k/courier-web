from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from clients.models import Client
from drivers.models import Driver

class Valoration(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='motorizado')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='cliente')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='valoración')
    experience = models.TextField(max_length=250, verbose_name='experiencia')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='fecha de creación')

    def __str__(self) -> str:
        return self.driver.full_name()

    class Meta:
        verbose_name = 'valoración'
        verbose_name_plural = 'valoraciones'