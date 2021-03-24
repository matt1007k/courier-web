from django import forms
from .models import Order

class CreateOrderClientModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'shippining'
            'total'
        )