from django import forms
from django.forms import models
from drivers.models import Driver, PaymentAccount, Vehicle

class DriverModelForm(forms.ModelForm):
    address_gps = forms.CharField(max_length=200, widget=forms.HiddenInput())
    class Meta:
        model = Driver
        fields = (
            'first_name', 
            'last_name', 
            'dni', 
            'address', 
            'cell_phone', 
            'cell_phone2', 
            'references', 
            'district', 
            'address_gps'
        )
        # widgets = {
        #     'address_gps': forms.HiddenInput(),
        # }


class VehicleModelForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = (
            'serial_number',
            'license_code',
            'license_plate_number'
        )

class PaymentAccountModelForm(forms.ModelForm):
    class Meta:
        model = PaymentAccount
        fields = (
            'bank',
            'account_number',
            'bank_account_number',
            'owners',
            'dni'
        )
