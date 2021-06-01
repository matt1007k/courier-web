import threading
from typing import Any, Dict
from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q
from django.core.serializers import serialize

from drivers.forms import DriverModelForm, PaymentAccountModelForm, VehicleModelForm

from .models import Driver, Vehicle
from authentication.models import User

from .utils import generate_driver_code
from orders.mails import Mail

class DriverListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'drivers/index.html'
    paginate_by = 10
    model = Driver
    permission_required = 'drivers.view_driver'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Motorizados'

        return context

    def query(self):
        return self.request.GET.get('q')
        
    def query_date(self):
        return self.request.GET.get('date')

    def get_queryset(self):
        if self.query():
            filters = Q(dni__icontains=self.query()) | Q(last_name__icontains=self.query()) | Q(first_name__icontains=self.query()) | Q(cell_phone__icontains=self.query()) 
            object_list = self.model.objects.filter(filters)
        elif self.query_date():
            filters = Q(created_at__date=self.query_date())
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


@login_required()
@permission_required('drivers.add_driver')
def driver_create_view(request, pk):
    title = 'Registrar motorizado'
    template_name = 'drivers/create.html'
    form_class = DriverModelForm(request.POST or None)
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST' and form_class.is_valid():
        code = generate_driver_code()
        if 'address_gps' in request.POST:
            address_gps = request.POST.get('address_gps') 
        driver = Driver.objects.create(
            code=code,
            user=user,   
            first_name = form_class.cleaned_data['first_name'],
            last_name = form_class.cleaned_data['last_name'],
            dni = form_class.cleaned_data['dni'],
            cell_phone = form_class.cleaned_data['cell_phone'],
            cell_phone2 = form_class.cleaned_data['cell_phone2'],
            address = form_class.cleaned_data['address'],
            district = form_class.cleaned_data['district'],
            references = form_class.cleaned_data['references'],
            address_gps=address_gps,
        )
        return redirect('drivers:payment-account', slug=str(driver.slug))

    return render(request, template_name, context={
        'title': title,
        'form': form_class,
        'user': user
    })
    
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
        if 'address_gps' in self.request.POST:
            form.instance.address_gps = self.request.POST.get('address_gps')
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
        thread = threading.Thread(
            target=Mail.send_verify_account_email,
            args=(driver.user, request)
        )
        thread.start()
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


def get_driver_view(request):
    if request.method == 'GET':
        q = request.GET.get('q')
        filters = Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(dni__icontains=q) | Q(district__icontains=q)
        qs = Driver.objects.filter(filters)[:5]
        data = serialize('json', qs)
        return HttpResponse(data, content_type='application/json')
    