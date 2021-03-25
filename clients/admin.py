from django.contrib import admin

from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'driver_code', 'user',)

admin.site.register(Client, ClientAdmin)