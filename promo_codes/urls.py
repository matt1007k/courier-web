from django.urls import path

from .views import validate_code_view

app_name='promo_codes'

urlpatterns = [
    path('validate/', validate_code_view)
]