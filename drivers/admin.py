from django.contrib import admin

from .models import Driver, Vehicle, PaymentAccount
from driver_payments.models import DriverPayment, DriverPaymentRate

class DriverAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'dni', 'address', 'user')
    fields = (
        'user', 'code', 'first_name', 'last_name', 'dni', 'address', 'cell_phone', 'cell_phone2', 'address_gps', 'references', 'district', 
    )

class PaymentAccountAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'dni', 'account_number', 'bank')

class DriverPaymentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'count_orders', 'total', 'created_at')

class DriverPaymentRateAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'min', 'max')

admin.site.register(Driver, DriverAdmin)
admin.site.register(PaymentAccount, PaymentAccountAdmin)
admin.site.register(Vehicle)
admin.site.register(DriverPayment, DriverPaymentAdmin)
admin.site.register(DriverPaymentRate, DriverPaymentRateAdmin)