from django.db.models.query import QuerySet
from addresses.models import Address
from django.urls.base import is_valid_path
from addresses.forms import AddressModelForm
from django.shortcuts import get_object_or_404, redirect, render
from authentication.models import User
from typing import Any, Dict
from django.contrib.auth.decorators import login_required, permission_required
from django.http.response import HttpResponse
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import DeleteView, UpdateView

from django.db.models import Q
from django.core.serializers import serialize

from .models import Client
from .forms import ClientModelForm

class ClientListVew(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = "clients/index.html"
    model = Client 
    paginate_by = 10
    permission_required = 'clients.view_client'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clientes'

        return context

    def get_queryset(self) -> QuerySet:
        object_list = self.model.objects.all().order_by("-id")
        #search
        object_list = object_list.search(self.query())
        return object_list

    def query(self):
        return self.request.GET.get('q')

    def query_address(self):
        return self.request.GET.get('address')

@login_required()
@permission_required('clients.add_client', raise_exception=True)
def client_create_view(request, pk):
    title = 'Registrar cliente'
    template_name = 'clients/create.html'
    form_class = ClientModelForm(request.POST or None)
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST' and form_class.is_valid():
        client = Client.objects.create(
            user=user,   
            first_name = form_class.cleaned_data['first_name'],
            last_name = form_class.cleaned_data['last_name'],
            cell_phone = form_class.cleaned_data['cell_phone'],
            driver_code = form_class.cleaned_data['driver_code'],
            store_name = form_class.cleaned_data['store_name'],
            logo = request.FILES['logo'] if 'logo' in request.FILES else None
        )
        return redirect('clients:complete-address', slug=client.slug)

    return render(request, template_name, context={
        'title': title,
        'form': form_class,
        'user': user
    })


class ClientDetailView(LoginRequiredMixin, DetailView):
    template_name = 'clients/detail.html'
    model = Client

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Perfil del cliente'
        return context 

class ClientUpdateView(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'clients/edit.html'
    form_class = ClientModelForm
    model = Client
    success_message = 'Registro editado con éxito'
    permission_required = 'clients.change_client'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar cliente'
        return context 

    def get_success_url(self) -> str:
        return reverse('clients:complete-address-update', kwargs={
            'slug': self.object.slug
        }) 

class ClientDeleteView(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'clients/delete.html'
    model = Client
    permission_required = 'clients.delete_client'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar cliente'
        return context 

    def get_success_url(self) -> str:
        messages.success(self.request, 'Registro eliminado con éxito')
        return reverse('clients:index')

def get_clients_view(request):
    if request.method == 'GET':
        q = request.GET.get('q')
        filters = Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(cell_phone__icontains=q)
        qs = Client.objects.filter(filters)[:5]
        data = serialize('json', qs)
        return HttpResponse(data, content_type='application/json')

@login_required()
@permission_required('addresses.add_address', raise_exception=True)
def complete_address_client_view(request, slug):
    title = 'Agregar dirección principal'
    template_name = 'clients/complete-address.html'
    form_class = AddressModelForm(request.POST or None)
    client = get_object_or_404(Client, slug=slug)

    if request.method == 'POST' and form_class.is_valid():
        form = form_class.save(commit=False)
        form.client = client
        form.default = True
        form.address_gps = request.POST.get('address_gps')
        form.save()

        messages.success(request, 'Registro completado con exíto')
        return redirect('clients:index')

    return render(request, template_name, context={
        'title': title,
        'form': form_class,
        'client': client
    })

@login_required()
@permission_required('addresses.change_address', raise_exception=True)
def complete_address_client_update_view(request, slug):
    title = 'Editar dirección principal'
    template_name = 'clients/complete-address-update.html'
    client = get_object_or_404(Client, slug=slug)
    form_class = AddressModelForm(request.POST or None, instance=client.address_default)

    if request.method == 'POST' and form_class.is_valid():
        form = form_class.save(commit=False)
        form.address_gps = request.POST.get('address_gps')
        form.save()

        messages.success(request, 'Registro editado con exíto')
        return redirect('clients:index')

    return render(request, template_name, context={
        'title': title,
        'form': form_class,
        'client': client
    })
    