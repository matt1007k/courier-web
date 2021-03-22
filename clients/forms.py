from django import forms
from django.forms import fields

from .models import Client

class ClientModelForm(forms.ModelForm):
    class Meta:
        model = Client 
        fields = (
            'first_name',
            'last_name',
            'address',
            'address_gps',
            'logo',
            'store_name',
            'driver_code',
            'social_media'
        )

class ClientRegisterForm(forms.ModelForm):
    class Meta:
        model = Client 
        fields = (
            'first_name',
            'last_name',
            'address',
            'logo',
            'store_name',
            'driver_code',
            'social_media'
        )