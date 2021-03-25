from django.contrib import admin

from .models import Driver, Vehicle

class DriverAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'dni', 'address', 'user')
    fields = (
        'user', 'code', 'first_name', 'last_name', 'dni', 'address', 'cell_phone', 'cell_phone2', 'address_gps', 'references', 'district', 'payment_account'
    )

admin.site.register(Driver, DriverAdmin)
admin.site.register(Vehicle)