from typing import Any, Dict
from django.db.models.query import QuerySet
from django.db.models import Q
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import DeleteView, UpdateView

from .models import Address
from .forms import AddressModelForm

class AddressListView(LoginRequiredMixin, ListView):
    template_name = 'addresses/index.html'
    paginate_by = 10
    model = Address

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Direcciones'

        return context

    def query(self):
        return self.request.GET.get('q')

    def get_queryset(self) -> QuerySet:
        client = self.request.user.client
        if client:
            if self.query():
                filters = Q(address__icontains=self.query()) | Q(district__icontains=self.query()) | Q(city__icontains=self.query()) | Q(reference__icontains=self.query())
                object_list = self.model.objects.filter(client=client).filter(filters).order_by('-default') 
            else: 
                object_list = self.model.objects.filter(client=client).order_by('-default')
        else:
            object_list = self.model.objects.all()
        return object_list 

class AddressCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'addresses/create.html'
    form_class = AddressModelForm
    success_message = 'Registro creado con exitó'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar dirección'

        return context

    def get_success_url(self) -> str:
        return reverse('addresses:index')

    def form_valid(self, form: AddressModelForm) -> HttpResponse:
        form.instance.client = self.request.user.client 
        return super().form_valid(form)

class AddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'addresses/edit.html'
    form_class = AddressModelForm
    model = Address
    success_message = 'Registro editado con exitó'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar dirección'

        return context

    def get_success_url(self) -> str:
        return reverse('addresses:index')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.client.id != self.get_object().client_id:
            return redirect('addresses:index')
        return super(AddressUpdateView, self).dispatch(request, *args, **kwargs)

class AddressDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'addresses/delete.html'
    model = Address

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Eliminar dirección'

        return context

    def get_success_url(self) -> str:
        messages.success(self.request, 'Registro eliminado con exitó')
        return reverse('addresses:index')

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.client.id != self.get_object().client_id:
            return redirect('addresses:index')
        return super(AddressDeleteView, self).dispatch(request, *args, **kwargs)

@login_required()
def default_view(request, pk):
    address = get_object_or_404(Address, pk=pk)

    if request.user.client.id != address.client_id:
        return reverse('addresses:index')

    if request.user.client.has_address_default():
        request.user.client.address_default.update_default()
    address.update_default(True)

    messages.success(request, 'Dirección principal actualizada')
    return redirect('addresses:index')