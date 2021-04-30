from django.contrib import admin

from .models import AssignOrder, Order
from details.models import Detail

class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'client')

class AssignOrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'driver', 'admin')

admin.site.register(Order, OrderAdmin)
admin.site.register(Detail)
admin.site.register(AssignOrder, AssignOrderAdmin)