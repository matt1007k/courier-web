from django.contrib import admin

from .models import Order
from details.models import Detail

class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'client')

admin.site.register(Order)
admin.site.register(Detail)