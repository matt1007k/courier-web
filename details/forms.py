from django import forms

from .models import Detail, PackageDelivered

class DetailForm(forms.Form):
    size = forms.CharField(max_length=150, label='Tamaño del paquete', widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    contain = forms.CharField(max_length=100, label='¿Qué contiene?', widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    value = forms.CharField(max_length=150, label='Valor del paquete' ,widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    image = forms.ImageField(required=False, label='Imagen del paquete (opcional)', widget=forms.FileInput(attrs={
        'class': 'input'
    }))
    description = forms.CharField(required=False, max_length=200, label='Nota (opcional)' ,widget=forms.Textarea(attrs={
        'class': 'input'
    }))

class PackageStatusModelForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = (
            'status',
        )

class DetailModelForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = (
            'size',
            'contain',
            'value',
            'image',
            'description',
        )

class PackageDeliveredModelForm(forms.ModelForm):
    class Meta:
        model = PackageDelivered
        fields = (
            'image',
            'image2',
            'description'
        )