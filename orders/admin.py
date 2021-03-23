from django.contrib import admin

from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'client')

admin.site.register(Order)