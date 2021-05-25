from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class UserAdminCustom(UserAdmin):
    list_display = ('__str__', 'email', 'is_active',)
    # model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Verificar cuenta', {'fields': ('is_email_verified',)}),
    )
    
admin.site.register(User, UserAdminCustom)