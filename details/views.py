import decimal
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import DeleteView
from django.urls import reverse 

from .models import AssignDeliveryAddress, AssignOriginAddress, Detail, UnassignDeliveryAddress
from addresses.models import Address

from .forms import DetailForm, DetailModelForm, PackageDeliveredModelForm
from addresses.forms import OriginAddressForm, DestinyAddressForm

from orders.utils import fields_destiny_form, get_or_create_order, fields_origin_form

@login_required()
@permission_required('details.add_detail', login_url='/orders/')
def create_detail_view(request):
    template = 'details/create.html'
    info_form = DetailModelForm(request.POST or None)
    origin_form = OriginAddressForm(request.POST or None)
    destiny_form = DestinyAddressForm(request.POST or None)
    order = get_or_create_order(request)
    client = order.client 
    my_addressess_list = Address.objects.filter(client=client).order_by('-id')
    if request.method == 'POST' and info_form.is_valid() and origin_form.is_valid()  and destiny_form.is_valid():
        address_origin = Address.objects.update_or_create_address_origin(client, origin_form.cleaned_data)
        address_destiny = Address.objects.update_or_create_address_destiny(client, destiny_form.cleaned_data)
        detail = Detail.objects.create(
            order=order, 
            size = request.POST.get('size'),
            contain = request.POST.get('contain'),
            value = request.POST.get('value'),
            image = request.FILES['image'] if 'image' in request.FILES else None,
            description = request.POST.get('description'),
            address_origin=address_origin,
            address_destiny=address_destiny,
            distance=request.POST.get('distance'),
            price_rate=request.POST.get('price_rate'),
        )
        if not detail is None:
            messages.success(request, 'La dirección de envío fue agregado con éxito.')
            return redirect('orders:add-addresses')


    return render(request, template, context={
        'order': order,
        'info_form': info_form,
        'origin_form': origin_form,
        'destiny_form': destiny_form,
        'my_addressess_list': my_addressess_list,
        'title': '¿Qué estas enviando?'
    })

@login_required()
@permission_required('details.change_detail', login_url='/orders/')
def update_detail_view(request, pk):
    template = 'details/update-client.html'    
    detail_obj = get_object_or_404(Detail, pk=pk)
    
    order = get_or_create_order(request)
    client = order.client
    info_form = DetailModelForm(request.POST or None, instance=detail_obj)
    origin_form = OriginAddressForm(request.POST or None, initial=fields_origin_form(detail=detail_obj))
    destiny_form = DestinyAddressForm(request.POST or None, initial=fields_destiny_form(detail=detail_obj))    
    my_addressess_list = Address.objects.filter(client=client).order_by('-id')

    if request.method == 'POST' and info_form.is_valid() and origin_form.is_valid()  and destiny_form.is_valid():
        # detail_obj.distance=12.00,
        # detail_obj.sub_total=10.00
        detail_obj.update_information(order, info_form.instance, request.POST.get('distance'), request.POST.get('price_rate'))
        detail_obj.update_addressess(client, origin_form.cleaned_data, destiny_form.cleaned_data)
        if 'image' in request.FILES:
            finfo = info_form.save(commit=False)
            finfo.image = request.FILES['image']
            finfo.save()

        messages.success(request, 'La dirección de envío fue editado con éxito.')
        return redirect('orders:add-addresses')

    return render(request, template, context={
        'order': order,
        'detail_obj': detail_obj,
        'info_form': info_form,
        'origin_form': origin_form,
        'destiny_form': destiny_form,
        'my_addressess_list': my_addressess_list,
        'title': '¿Qué estas enviando?'
    })

class DeleteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'details/delete.html'
    permission_required = 'details.delete_detail'

    def get_success_url(self) -> str:
        messages.success(self.request, "La dirección de envío fue eliminado con éxito")
        return self.request.GET.get('next', reverse('orders:add-addresses'))

    def get_queryset(self):
        return Detail.objects.all()

@login_required()
def origin_map_view(request, pk):
    title = 'Ver mapa de dirección de recojo'
    template_name = 'details/origin-map.html'
    detail = Detail.objects.get(pk=pk) 
    if not detail.is_delivered:
        detail.on_routed()
    driver = AssignOriginAddress.objects.filter(detail=detail).first().driver

    return render(request, template_name, context={
        'title': title,
        'detail': detail,
        'driver': driver
    })

@login_required()
def destiny_map_view(request, pk):
    title = 'Ver mapa de dirección de entrega'
    template_name = 'details/destiny-map.html'
    detail = Detail.objects.get(pk=pk) 
    if not detail.is_delivered:
        detail.on_routed()
    driver = AssignDeliveryAddress.objects.filter(detail=detail).first().driver

    return render(request, template_name, context={
        'title': title,
        'detail': detail,
        'driver': driver
    })

@login_required()
@permission_required('details.view_assignoriginaddress', raise_exception=True)
def received_package_view(request, pk):
    if request.method == 'GET':
        detail = Detail.objects.get(pk=pk)
        detail.received()
        UnassignDeliveryAddress.objects.create(
            detail=detail
        )

        messages.success(request, 'El paquete ha sido recojido')
        return redirect('orders:origins')

@login_required()
@permission_required('details.view_assignoriginaddress', raise_exception=True)
def not_on_routed_origin_view(request, pk):
    if request.method == 'GET':
        detail = Detail.objects.get(pk=pk)
        if not detail.is_delivered:
            detail.pended()

        return redirect('orders:origins')

@login_required()
@permission_required('details.view_assigndeliveryaddress', raise_exception=True)
def not_on_routed_delivery_view(request, pk):
    if request.method == 'GET':
        detail = Detail.objects.get(pk=pk)
        if not detail.is_delivered:
            detail.pended()

        return redirect('orders:deliveries')

@login_required()
@permission_required('details.add_packagedelivered', raise_exception=True)
def package_delivered_view(request, pk):
    title = 'Entrega de paquete'
    template_name = 'orders/assign/delivered.html'
    detail = Detail.objects.get(pk=pk)
    form_class = PackageDeliveredModelForm(request.POST, request.FILES)
    if request.method == 'POST' and form_class.is_valid():
        print('post', request.FILES)
        form = form_class.save(commit=False)
        form.detail = detail
        form.driver = request.user.driver if request.user.is_driver else None
        form.save()
        detail.delivered()
        messages.success(request, 'El paquete fue registrado como entregado')
        return redirect('orders:deliveries')

    return render(request, template_name, context={
        'title': title,
        'form': form_class,
        'detail': detail
    })



