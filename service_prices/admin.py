from django.contrib import admin

from .models import ServicePrice

class ServicePriceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'min', 'max')

admin.site.register(ServicePrice, ServicePriceAdmin)