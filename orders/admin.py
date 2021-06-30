from django.contrib import admin

from .models import Order
from details.models import (
    AssignOriginAddress, AssignDeliveryAddress, Detail,
    UnassignOriginAddress, UnassignDeliveryAddress, PackageDelivered, TrackingOrder
)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'client')

class DetailAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ('__str__', 'client', 'price_rate', 'distance', 'created_at')
    search_fields = [
        'client__first_name', 
        'client__last_name', 
        'tracking_code', 
        'size', 
        'contain', 
        'value', 
        'description',
        'address_origin__full_name',
        'address_origin__cell_phone',
        'address_origin__address',
        'address_destiny__full_name',
        'address_destiny__cell_phone',
        'address_destiny__address',
    ]
    list_filter = ('status', 'created_at')

class UnassingOriginAddressAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ('__str__', 'detail')
class UnassingDeliveryAddressAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ('__str__', 'detail')

class AssingOriginAddressAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ('detail', 'driver', 'admin', 'is_received', 'created_at')
    search_fields = [
        'detail__tracking_code', 
        'detail__size', 
        'detail__contain', 
        'detail__value', 
        'detail__description',
        'driver__first_name',
        'driver__last_name',
        'driver__dni',
    ]
    list_filter = ('is_received', 'created_at')
class AssingDeliveryAddressAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ('detail', 'driver', 'admin', 'is_delivered', 'created_at')
    search_fields = [
        'detail__tracking_code', 
        'detail__size', 
        'detail__contain', 
        'detail__value', 
        'detail__description',
        'driver__first_name',
        'driver__last_name',
        'driver__dni',
    ]
    list_filter = ('is_delivered', 'created_at')

class PackageDeliveredAdmin(admin.ModelAdmin):
    ordering = ['-id']
    list_display = ('__str__', 'detail', 'driver', 'created_at')
    search_fields = [
        'detail__tracking_code', 
        'detail__size', 
        'detail__contain', 
        'detail__value', 
        'detail__description',
        'driver__first_name',
        'driver__last_name',
        'driver__dni',
        'description',
    ]
    list_filter = ('created_at',)

class TrackingOrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'location', 'created_at')

admin.site.register(Order, OrderAdmin)
admin.site.register(Detail, DetailAdmin)
admin.site.register(UnassignOriginAddress, UnassingOriginAddressAdmin)
admin.site.register(UnassignDeliveryAddress, UnassingDeliveryAddressAdmin)
admin.site.register(AssignOriginAddress, AssingOriginAddressAdmin)
admin.site.register(AssignDeliveryAddress, AssingDeliveryAddressAdmin)
admin.site.register(PackageDelivered, PackageDeliveredAdmin)
admin.site.register(TrackingOrder, TrackingOrderAdmin)