from django.contrib import admin

from .models import Setting

class SettingAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'can_you_create_orders', 'time_limit_from', 'time_limit_to')

admin.site.register(Setting, SettingAdmin)
