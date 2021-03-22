from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls.base import reverse
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages

from .forms import CustomUserForm, RegisterForm
from clients.forms import ClientRegisterForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            return redirect('dash')
        else: 
            messages.error(request, 'Usuario y/o contraseña incorrecto')

    return render(request, 'auth/login.html', context={})

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada con exitó.')
    return redirect('auth:login')

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():

        user = form.save()
        if user:
            login(request, user)
            messages.success(request, 'Cuenta creada con exitó')
            return redirect('auth:complete-info')
        
    return render(request, 'auth/register.html', context={
        'form': form
    })

class CompleteInfoClientView(LoginRequiredMixin, CreateView):
    template_name = 'auth/complete-info.html'
    form_class = ClientRegisterForm

    def get_success_url(self) -> str:
        messages.success(self.request, 'Bienvenido {}'.format(self.request.user.username))
        return reverse("dash")
    
    def form_valid(self, form: ClientRegisterForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

class UserCreateView(LoginRequiredMixin, CreateView):
    template_name = 'auth/create.html'
    form_class = CustomUserForm

    def get_success_url(self) -> str:
        messages.success(self.request, 'Usuario registrado con exitó')
        return self.request.GET.get('next', reverse('auth:create'))


