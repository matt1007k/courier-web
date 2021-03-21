from django import forms
from drivers.models import Driver, Vehicle

class DriverModelForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = (
            'user', 'code', 'first_name', 'last_name', 'dni', 'address', 'cell_phone', 'cell_phone2', 'current_address', 'references', 'district', 'avatar', 'payment_account'
        )


class VehicleModelForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = (
            'serial_number',
            'license_code',
            'license_plate_number'
        )
