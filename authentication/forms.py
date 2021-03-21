from django import forms
# from .models import User as 
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, min_length=4, max_length=50,
                            label='Nombre de usuario',
                            widget=forms.TextInput(attrs={
                                'class': 'input'
                            }))
    email = forms.EmailField(required=True, label="Correo electrónico",
                             widget=forms.EmailInput(attrs={
                                 'class': 'input'
                             }))
    password = forms.CharField(required=True, 
                            label='Contraseña',
                            widget=forms.PasswordInput(attrs={
                                'class': 'input'
                            }))

    password2 = forms.CharField(required=True, label="Repetir contraseña",
                            widget=forms.PasswordInput(attrs={
                                'class': 'input'
                            }))

    def clean_username(self):
        username: str = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya está en uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El correo electrónico ya está en uso.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'La contraseña no coincide')

    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )

class UserModelForm(forms.ModelForm):
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={
        'class': 'input'
    }))
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',)