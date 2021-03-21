from typing import Any
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q

from drivers.forms import DriverModelForm, VehicleModelForm

from .models import Driver, Vehicle

class DriverListView(LoginRequiredMixin, ListView):
    template_name = 'drivers/index.html'
    paginate_by = 10
    # queryset = Driver.objects.all().order_by('-id')
    model = Driver

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Motorizados'

        return context

    def query(self):
        return self.request.GET.get('q')

    def get_queryset(self):
        if self.query():
            filters = Q(dni__icontains=self.query()) | Q(last_name__icontains=self.query())
            object_list = self.model.objects.filter(filters)
        else:
            object_list = self.model.objects.all().order_by('-id')
        return object_list

class DriverDetailView(DetailView):
    model = Driver
    template_name = 'drivers/detail.html'


class DriverCreateView(LoginRequiredMixin, CreateView):
    template_name = 'drivers/create.html'
    form_class = DriverModelForm

    def get_success_url(self) -> str:
        messages.success(self.request, "Registro realizado con exitó")
        return reverse('drivers:index')

    # def form_valid(self, form: DriverModelForm) -> HttpResponse:
    #     # form.save()
    #     # driver = form.save(commit=False) # instance
    #     # self.request.user
    #     # driver.field = value
    #     # driver.save()
    #     return super(DriverModelForm, self).form_valid(form)
    
class DriverUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'drivers/edit.html'
    form_class = DriverModelForm
    model = Driver

    def get_success_url(self) -> str:
        messages.success(self.request, "Registro editado con exitó")
        return reverse('drivers:index')

class DriverDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'drivers/delete.html'

    def get_success_url(self) -> str:
        messages.success(self.request, "Registro eliminado con exitó")
        return reverse('drivers:index')

    def get_queryset(self):
        return Driver.objects.all()


class VehicleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'vehicles/create.html'
    form_class = VehicleModelForm

    def get_success_url(self) -> str:
        messages.success(self.request, "Moto registrado con exitó")
        return reverse('drivers:detail')
    
    def form_valid(self, form: VehicleModelForm) -> HttpResponse:
        vehicle = form.save(commit=False)
        vehicle.driver = self.request.user.driver
        vehicle.save()
        return super(VehicleModelForm, self).form_valid(form)

class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'vehicles/edit.html'
    form_class = VehicleModelForm
    model = Vehicle

    def get_success_url(self) -> str:
        messages.success(self.request, "Moto editado con exitó")
        return self.request.GET.get('next', reverse('drivers:index'))
    