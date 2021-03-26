from django import forms

from .models import Address

class AddressModelForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            'address',
            'district',
            'city',
            'reference'
        )

class OriginAddressForm(forms.Form):
    origin_address = forms.CharField(label='Dirección', max_length=100, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    origin_district = forms.CharField(label='Distrito', max_length=100, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    origin_city = forms.CharField(label='Ciudad', max_length=100, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    origin_reference = forms.CharField(label='Referencia', max_length=100, widget=forms.Textarea(attrs={
        'class': 'input'
    }))

class DestinyAddressForm(forms.Form):
    destiny_address = forms.CharField(label='Dirección', max_length=100, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    destiny_district = forms.CharField(label='Distrito', max_length=100, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    destiny_city = forms.CharField(label='Ciudad', max_length=100, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    destiny_reference = forms.CharField(label='Referencia', max_length=100, widget=forms.Textarea(attrs={
        'class': 'input'
    }))
