from django.contrib import admin
from django.db.models import fields
from .models import Valoration

class ValorationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'rating', 'client', 'created_at')

admin.site.register(Valoration, ValorationAdmin)