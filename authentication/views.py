import threading
from orders.mails import Mail
from typing import Any, Dict
from django.core.mail import message
from django.http import HttpResponse, request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls.base import reverse
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import PermissionSerializer

from django.utils.encoding import force_text
from .utils import generate_token

from django.contrib import messages

from django.contrib.auth.models import Group, Permission
from .models import User
from .forms import CustomUserForm, RegisterForm
from clients.forms import ClientRegisterForm
from addresses.forms import AddressModelForm

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            # if not user.is_email_verified:
            #     messages.success(request, 'Hemos enviado un correo, para verificar tu correo electrónico')
            #     logout(request)
            #     return redirect('auth:login')
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
    form = CustomUserForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if user:
            client_group = Group.objects.get(name='Cliente')
            user.groups.add(client_group)
            login(request, user)
            return redirect('auth:complete-info')
    # else:
        # Append css class to every field that contains errors.
        # for field in form.errors:
        #     form[field].field.widget.attrs['class'] += ' is-invalid'
        
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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self) -> str:
        # if not self.request.user.is_email_verified:
        #     thread = threading.Thread(
        #         target=Mail.send_verify_account_email,
        #         args=(self.request.user, self.request)
        #     )
        #     thread.start()
        #     logout(self.request)
        #     messages.success(self.request, 'Te hemos enviado un correo, para activar y verificar tu correo electrónico')
        #     return reverse('auth:login')
        messages.success(self.request, 'Bienvenido {}'.format(self.request.user.username))
        return reverse('dash')
    
    def form_valid(self, form: AddressModelForm) -> HttpResponse:
        form.instance.client = self.request.user.client
        form.instance.default = True
        form.instance.address_gps = self.request.POST.get('address_gps')
        return super().form_valid(form)

class UserCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'auth/create.html'
    form_class = CustomUserForm
    permission_required = 'authentication.add_user'

    def get_success_url(self) -> str:
        self.model.set_driver()
        messages.success(self.request, 'Usuario registrado con éxito')
        print('user', self.model.pk)
        return redirect('drivers:create', kwargs={
            'pk': self.model.pk
        })

    def form_invalid(self, form: CustomUserForm) -> HttpResponse:
        return super().form_invalid(form)


@login_required()
@permission_required('authentication.add_user', raise_exception=True)
def user_create_view(request):
    template_name = 'auth/create.html'
    form_class = CustomUserForm(request.POST or None)

    if request.method == 'POST' and form_class.is_valid():
        user = form_class.save()
        user.set_driver()
        messages.success(request, 'Usuario registrado con éxito')
        return redirect('drivers:create', pk=user.pk)

    return render(request, template_name, context={
        'form': form_class
    })

@login_required()
@permission_required('authentication.add_user', raise_exception=True)
def user_create_client_view(request):
    template_name = 'auth/create-client.html'
    form_class = CustomUserForm(request.POST or None)

    if request.method == 'POST' and form_class.is_valid():
        user = form_class.save()
        user.set_client()
        messages.success(request, 'Usuario registrado con éxito')
        return redirect('clients:create', pk=user.pk)

    return render(request, template_name, context={
        'form': form_class
    })

def activate_user(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.success(request, 'Correo electrónico verificado con exíto, ya puedes ingresar')
        return redirect('auth:login')
    template_name = 'auth/activate-failed.html'

    return render(request, template_name, context={})

class PermissionAuthListApiView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        auth = request.user
        permission_auth = auth.user_permissions.all()
        try:
            permission_group = auth.groups.first().permissions.all()
            sr = PermissionSerializer(permission_group | permission_auth, many=True)

            return Response(sr.data)
        except AttributeError:
            print('errors')

        sr = PermissionSerializer(permission_auth, many=True)
        return Response(sr.data)