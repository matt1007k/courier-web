from django import forms

from .models import Detail

class DetailForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='Nombre', widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    last_name = forms.CharField(max_length=100, label='Apellidos', widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    email = forms.EmailField(max_length=100, label='Correo electrónico' ,widget=forms.EmailInput(attrs={
        'class': 'input'
    }))
    cell_phone = forms.CharField(max_length=9, label='Num. de celular' ,widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    image = forms.ImageField(required=False, label='Imagen del paquete (opcional)', widget=forms.FileInput(attrs={
        'class': 'input'
    }))
    description = forms.CharField(max_length=150, label='Descripción del paquete' ,widget=forms.Textarea(attrs={
        'class': 'input'
    }))

class DetailModelForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = (
            'first_name',
            'last_name',
            'email',
            'cell_phone',
            'image',
            'description',
        )