from typing import Any, Dict
from django.http import request
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q

from drivers.forms import DriverModelForm, VehicleModelForm

from .models import Driver, Vehicle

from .utils import generate_driver_code

class DriverListView(LoginRequiredMixin, ListView):
    template_name = 'drivers/index.html'
    paginate_by = 10
    model = Driver
    # permission_required = 'drivers.view_driver'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Motorizados'

        return context

    def query(self):
        return self.request.GET.get('q')

    def get_queryset(self):
        if self.query():
            filters = Q(dni__icontains=self.query()) | Q(last_name__icontains=self.query()) | Q(first_name__icontains=self.query())
            object_list = self.model.objects.filter(filters)
        else:
            object_list = self.model.objects.all().order_by('-id')
        return object_list

class DriverDetailView(DetailView):
    model = Driver
    template_name = 'drivers/detail.html'


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Perfil del motorizado'
        return context


class DriverCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'drivers/create.html'
    form_class = DriverModelForm
    permission_required = 'drivers.add_driver'

    def get_success_url(self) -> str:
        messages.success(self.request, "Registro realizado con éxito")
        return reverse('drivers:index')

    def form_valid(self, form: DriverModelForm) -> HttpResponse:
        form.instance.code = generate_driver_code()
        return super().form_valid(form)
    
class DriverUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'drivers/edit.html'
    form_class = DriverModelForm
    model = Driver
    permission_required = 'drivers.change_driver'

    def get_success_url(self) -> str:
        messages.success(self.request, "Registro editado con éxito")
        return reverse('drivers:index')

class DriverDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'drivers/delete.html'
    permission_required = 'drivers.delete_driver'

    def get_success_url(self) -> str:
        messages.success(self.request, "Registro eliminado con éxito")
        return reverse('drivers:index')

    def get_queryset(self):
        return Driver.objects.all()


class VehicleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'vehicles/create.html'
    form_class = VehicleModelForm
    permission_required = 'drivers.add_vehicle'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar moto'
        return context

    def get_success_url(self) -> str:
        messages.success(self.request, "Moto registrado con éxito")
        return reverse('drivers:detail', kwargs={'slug':self.request.user.driver.slug})
    
    def form_valid(self, form: VehicleModelForm) -> HttpResponse:
        form.instance.driver = self.request.user.driver
        return super().form_valid(form)

class VehicleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'vehicles/edit.html'
    form_class = VehicleModelForm
    model = Vehicle
    permission_required = 'drivers.change_vehicle'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar moto'
        return context
    def get_success_url(self) -> str:
        messages.success(self.request, "Moto editado con éxito")
        return self.request.GET.get('next', reverse('drivers:detail', kwargs={'slug': self.request.user.driver.slug}))
    