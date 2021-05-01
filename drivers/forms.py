from django import forms
from drivers.models import Driver, PaymentAccount, Vehicle

class DriverModelForm(forms.ModelForm):
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
        )


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
