import datetime
from django.db import models

class Setting(models.Model):
	can_you_create_orders = models.BooleanField(default=False, verbose_name="¿puedes registrar pedidos?")
	time_limit_from = models.TimeField(default=datetime.time(23, 00), blank=True, verbose_name="tiempo de cierre del sistema")
	time_limit_to = models.TimeField(default=datetime.time(8, 00), blank=True, verbose_name="tiempo de abrir del sistema")
	message_origin = models.TextField(max_length=250, null=True, blank=True, verbose_name='mensaje para el cliente del recojo de sus paquetes')



	def __str__(self):
		return str(self.pk)

	def cannot_create_order(self):
		self.can_you_create_orders = True
		self.save()

	def can_create_order(self):
		self.can_you_create_orders = True
		self.save()


	class Meta:
		verbose_name = 'configuración'
		verbose_name_plural = 'configuraciones'
