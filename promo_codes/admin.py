from promo_codes.models import PromoCode
from django.contrib import admin


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'discount', 'valid_from', 'valid_to', 'used')
    exclude = ['code']

admin.site.register(PromoCode, PromoCodeAdmin)
