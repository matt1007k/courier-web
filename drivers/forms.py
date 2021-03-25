from django import forms
from drivers.models import Driver, Vehicle

class DriverModelForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = (
            'user', 'first_name', 'last_name', 'dni', 'address', 'cell_phone', 'cell_phone2', 'references', 'district', 'payment_account'
        )


class VehicleModelForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = (
            'serial_number',
            'license_code',
            'license_plate_number'
        )
