from django import forms
from django.core.validators import RegexValidator, validate_email

from .models import Address

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,9}$', message="El núm. de celular no es válido, es formato válido es: 999999999")

class AddressModelForm(forms.ModelForm):
    address_gps = forms.CharField(max_length=200, widget=forms.HiddenInput())
    class Meta:
        model = Address
        fields = (
            'full_name',
            'email',
            'cell_phone',
            'address',
            'district',
            'city',
            'address_detail',
            'reference',
            'address_gps'
        )

class OriginAddressForm(forms.Form):
    origin_full_name = forms.CharField(max_length=100, label='Nombre completo de la persona', widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    origin_email = forms.EmailField(validators=[validate_email],max_length=100, label='Correo electrónico' ,widget=forms.EmailInput(attrs={
        'class': 'input'
    }))
    origin_cell_phone = forms.CharField(validators=[phone_regex],max_length=9, label='Num. de celular' ,widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    origin_address = forms.CharField(label='Dirección', max_length=100, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    origin_district = forms.CharField(label='Distrito', max_length=100, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    origin_city = forms.CharField(label='Ciudad o País', max_length=100, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    origin_address_detail = forms.CharField(label='N° de puerta/Lte/Mz/Dpto/Piso', max_length=200, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    origin_reference = forms.CharField(label='Referencia', max_length=100, widget=forms.Textarea(attrs={
        'class': 'input'
    }))
    origin_position = forms.CharField(label=None,max_length=100, widget=forms.HiddenInput())

class DestinyAddressForm(forms.Form):
    destiny_full_name = forms.CharField(max_length=100, label='Nombre completo de la persona', widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    destiny_email = forms.EmailField(validators=[validate_email],max_length=100, label='Correo electrónico' ,widget=forms.EmailInput(attrs={
        'class': 'input'
    }))
    destiny_cell_phone = forms.CharField(validators=[phone_regex],max_length=9, label='Num. de celular' ,widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    destiny_address = forms.CharField(label='Dirección', max_length=100, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    destiny_district = forms.CharField(label='Distrito', max_length=100, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    destiny_city = forms.CharField(label='Ciudad o País', max_length=100, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    destiny_address_detail = forms.CharField(label='N° de puerta/Lte/Mz/Dpto/Piso', max_length=200, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    destiny_reference = forms.CharField(label='Referencia', max_length=100, widget=forms.Textarea(attrs={
        'class': 'input'
    }))
    destiny_position = forms.CharField(label=None,max_length=100, widget=forms.HiddenInput())
    price_rate = forms.CharField(label=None,max_length=100, widget=forms.HiddenInput())
    distance = forms.CharField(label=None,max_length=100, widget=forms.HiddenInput())
