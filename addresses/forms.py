from django import forms

from .models import Address

class AddressModelForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            'full_name',
            'email',
            'cell_phone',
            'address',
            'district',
            'city',
            'reference'
        )

class OriginAddressForm(forms.Form):
    origin_full_name = forms.CharField(max_length=100, label='Nombre completo de la persona', widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    origin_email = forms.EmailField(max_length=100, label='Correo electrónico' ,widget=forms.EmailInput(attrs={
        'class': 'input'
    }))
    origin_cell_phone = forms.CharField(max_length=9, label='Num. de celular' ,widget=forms.TextInput(attrs={
        'class': 'input'
    }))
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
    destiny_full_name = forms.CharField(max_length=100, label='Nombre completo de la persona', widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    destiny_email = forms.EmailField(max_length=100, label='Correo electrónico' ,widget=forms.EmailInput(attrs={
        'class': 'input'
    }))
    destiny_cell_phone = forms.CharField(max_length=9, label='Num. de celular' ,widget=forms.TextInput(attrs={
        'class': 'input'
    }))
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
