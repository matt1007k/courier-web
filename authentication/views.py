from typing import Any, Dict
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls.base import reverse
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib import messages

from .forms import CustomUserForm, RegisterForm
from clients.forms import ClientRegisterForm
from addresses.forms import AddressModelForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dash')
        else: 
            messages.error(request, 'Usuario y/o contraseña incorrecto')

    return render(request, 'auth/login.html', context={})

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada con éxito.')
    return redirect('auth:login')

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if user:
            client_group = Group.objects.get(name='Cliente')
            user.groups.add(client_group)
            login(request, user)
            return redirect('auth:complete-info')
    else:
        # Append css class to every field that contains errors.
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        
    return render(request, 'auth/register.html', context={
        'form': form
    })

class CompleteInfoClientView(LoginRequiredMixin, CreateView):
    template_name = 'auth/complete-info.html'
    form_class = ClientRegisterForm

    def get_success_url(self) -> str:
        return reverse('auth:complete-address')
    
    def form_valid(self, form: ClientRegisterForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

class CompleteAddressClientView(LoginRequiredMixin, CreateView):
    template_name = 'auth/complete-address.html'
    form_class = AddressModelForm

    def get_success_url(self) -> str:
        messages.success(self.request, 'Bienvenido {}'.format(self.request.user.username))
        return reverse('dash')
    
    def form_valid(self, form: AddressModelForm) -> HttpResponse:
        form.instance.client = self.request.user.client
        form.instance.default = True
        return super().form_valid(form)

class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'auth/create.html'
    form_class = CustomUserForm
    permission_required = 'authentication.add_user'

    def get_success_url(self) -> str:
        self.model.set_driver()
        messages.success(self.request, 'Usuario registrado con éxito')
        return self.request.GET.get('nex', reverse('drivers:create'))

    def form_invalid(self, form: CustomUserForm) -> HttpResponse:
        return super().form_invalid(form)


@login_required()
@permission_required('authentication.add_user', login_url='/drivers')
def user_create_view(request):
    template_name = 'auth/create.html'
    form_class = CustomUserForm(request.POST or None)

    if request.method == 'POST' and form_class.is_valid():
        user = form_class.save()
        if user:
            user.set_driver()
            messages.success(request, 'Usuario registrado con éxito')
            return request.GET.get('nex', redirect('drivers:create'))
        return reverse('drivers:create')

    return render(request, template_name, context={
        'form': form_class
    })
