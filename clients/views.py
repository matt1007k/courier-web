from typing import Any, Dict
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import DeleteView, UpdateView
from .models import Client
from .forms import ClientModelForm

class ClientListVew(LoginRequiredMixin, ListView):
    template_name = "clients/index.html"
    queryset = Client.objects.all().order_by("-id")
    paginate_by = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clientes'

        return context

class ClienteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'clients/create.html'
    form_class = ClientModelForm
    success_message = 'Registro creado con éxito'

    def get_success_url(self) -> str:
        return reverse('clients:index')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs) 
        context['title'] = 'Registrar cliente'
        return context


class ClientDetailView(LoginRequiredMixin, DetailView):
    template_name = 'clients/detail.html'
    model = Client

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Perfil del cliente'
        return context 

class ClientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'clients/edit.html'
    form_class = ClientModelForm
    model = Client
    success_message = 'Registro editado con éxito'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar cliente'
        return context 

    def get_success_url(self) -> str:
        return reverse('clients:index') 

class ClientDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'clients/delete.html'
    model = Client

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar cliente'
        return context 

    def get_success_url(self) -> str:
        messages.success(self.request, 'Registro eliminado con éxito')
        return reverse('clients:index')