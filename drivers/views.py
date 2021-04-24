import json
from typing import Any, Dict
from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.views.generic.base import View

from drivers.forms import DriverModelForm, PaymentAccountModelForm, VehicleModelForm

from .models import Driver, PaymentAccount, Vehicle

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrar motorizado'

        return context

    def get_success_url(self) -> str:
        # messages.success(self.request, "Registro realizado con éxito")
        return reverse('drivers:payment-account', kwargs={
            'slug': Driver.objects.last().slug
        })

    def form_valid(self, form: DriverModelForm) -> HttpResponse:
        form.instance.code = generate_driver_code()
        if 'position' in self.request.POST:
            form.instance.address_gps = json.loads(self.request.POST.get('position')) 
        return super().form_valid(form)
    
class DriverUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'drivers/edit.html'
    form_class = DriverModelForm
    model = Driver
    permission_required = 'drivers.change_driver'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar motorizado'

        return context

    def form_valid(self, form: DriverModelForm) -> HttpResponse:
        if 'position' in self.request.POST:
            form.instance.address_gps = json.loads(self.request.POST.get('position')) 
        return super().form_valid(form)

    def get_success_url(self) -> str:
        # messages.success(self.request, "Registro editado con éxito")
        return reverse('drivers:payment-account.update', kwargs={
            'slug': self.object.slug
        })

class DriverDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'drivers/delete.html'
    permission_required = 'drivers.delete_driver'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar motorizado'

        return context

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
    

@login_required()
@permission_required('drivers.add_paymentaccount', login_url='/drivers/create')
def payment_account_create_view(request, slug):
    template_name = 'payment_accounts/create.html'
    driver = Driver.objects.get(slug=slug)

    form_class = PaymentAccountModelForm(request.POST or None)
    title = 'Registrar cuenta de pago'

    if request.method == 'POST' and form_class.is_valid():
        form = form_class.save(commit=False)
        form.driver = driver
        form.save()
        messages.success(request, "Motorizado registrado con éxito")
        return redirect('drivers:index')

    return render(request, template_name, context={
        'title': title,
        'form': form_class
    })

@login_required()
@permission_required('drivers.change_paymentaccount', login_url='/drivers')
def payment_account_update_view(request, slug):
    template_name = 'payment_accounts/edit.html'
    driver = Driver.objects.get(slug=slug)

    form_class = PaymentAccountModelForm(request.POST or None, instance=driver.paymentaccount or None)
    title = 'Editar cuenta de pago'

    if request.method == 'POST' and form_class.is_valid():
        form_class.save()
        messages.success(request, "Motorizado editado con éxito")
        return redirect('drivers:index')

    return render(request, template_name, context={
        'title': title,
        'form': form_class
    })
    
    