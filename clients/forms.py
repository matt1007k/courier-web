from django import forms

from .models import Client
from drivers.models import Driver

class ClientModelForm(forms.ModelForm):
    class Meta:
        model = Client 
        fields = (
            'first_name',
            'last_name',
            'logo',
            'store_name',
            'driver_code',
            'social_media'
        )

    def clean_driver_code(self):
        driver_code: str = self.cleaned_data.get('driver_code')

        if not Driver.objects.filter(code=driver_code).exists():
            raise forms.ValidationError('El código de motorizado no existe.')
        return driver_code

class ClientRegisterForm(forms.ModelForm):
    class Meta:
        model = Client 
        fields = (
            'first_name',
            'last_name',
            'logo',
            'store_name',
            'driver_code',
        )
    def clean_driver_code(self):
        driver_code: str = self.cleaned_data.get('driver_code')

        if not Driver.objects.filter(code=driver_code).exists():
            raise forms.ValidationError('El código de motorizado no existe.')
        return driver_code