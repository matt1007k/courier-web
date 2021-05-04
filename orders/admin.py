from django.contrib import admin

from .models import Order
from details.models import (
    AssignOriginAddress, AssignDeliveryAddress, Detail,
    UnassignOriginAddress, UnassignDeliveryAddress, PackageDelivered
)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'client')

class UnassingOriginAddressAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'detail')
class UnassingDeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'detail')

class AssingOriginAddressAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'detail', 'driver', 'admin')
class AssingDeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'detail', 'driver', 'admin')

class PackageDeliveredAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'detail', 'driver', 'created_at')

admin.site.register(Order, OrderAdmin)
admin.site.register(Detail)
admin.site.register(UnassignOriginAddress, UnassingOriginAddressAdmin)
admin.site.register(UnassignDeliveryAddress, UnassingDeliveryAddressAdmin)
admin.site.register(AssignOriginAddress, AssingOriginAddressAdmin)
admin.site.register(AssignDeliveryAddress, AssingDeliveryAddressAdmin)
admin.site.register(PackageDelivered, PackageDeliveredAdmin)