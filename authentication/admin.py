from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class UserAdminCustom(UserAdmin):
    list_display = ('__str__', 'email', 'is_active',)

admin.site.register(User, UserAdminCustom)