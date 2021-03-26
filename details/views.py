from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django.urls import reverse 

from .models import Detail
from addresses.models import Address

from .forms import DetailForm, DetailModelForm
from addresses.forms import OriginAddressForm, DestinyAddressForm

from orders.utils import fields_destiny_form, get_or_create_order, fields_origin_form

@login_required()
def create_client_view(request):
    template = 'details/create-client.html'
    info_form = DetailForm(request.POST or None)
    origin_form = OriginAddressForm(request.POST or None)
    destiny_form = DestinyAddressForm(request.POST or None)
    client = request.user.client 
    my_addressess_list = Address.objects.filter(client=client).order_by('-id')
    if request.method == 'POST' and info_form.is_valid() and origin_form.is_valid()  and destiny_form.is_valid():
        order = get_or_create_order(request)
        address_origin = Address.objects.update_or_create_address_origin(client, origin_form.cleaned_data)
        address_destiny = Address.objects.update_or_create_address_destiny(client, destiny_form.cleaned_data)
        detail = Detail.objects.create(
            order=order, 
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            email = request.POST.get('email'),
            cell_phone = request.POST.get('cell_phone'),
            image = request.FILES['image'] if 'image' in request.FILES else None,
            description = request.POST.get('description'),
            address_origin=address_origin,
            address_destiny=address_destiny,
            distance=12,
            sub_total=10
        )
        if not detail is None:
            messages.success(request, 'El pedido de envío agregado con exitó.')
            return redirect('orders:create-client')


    return render(request, template, context={
        'info_form': info_form,
        'origin_form': origin_form,
        'destiny_form': destiny_form,
        'my_addressess_list': my_addressess_list
    })

@login_required()
def update_client_view(request, pk):
    template = 'details/update-client.html'    
    detail_obj = get_object_or_404(Detail, pk=pk)
    
    info_form = DetailModelForm(request.POST or None, instance=detail_obj)
    origin_form = OriginAddressForm(request.POST or None, initial=fields_origin_form(detail=detail_obj))
    destiny_form = DestinyAddressForm(request.POST or None, initial=fields_destiny_form(detail=detail_obj))    
    client = request.user.client 
    my_addressess_list = Address.objects.filter(client=client).order_by('-id')

    if request.method == 'POST' and info_form.is_valid() and origin_form.is_valid()  and destiny_form.is_valid():
        order = get_or_create_order(request)
        # detail_obj.distance=12.00,
        # detail_obj.sub_total=10.00
        detail_obj.update_information(order, info_form.instance)
        detail_obj.update_addressess(client, origin_form.cleaned_data, destiny_form.cleaned_data)
        if 'image' in request.FILES:
            finfo = info_form.save(commit=False)
            finfo.image = request.FILES['image']
            finfo.save()

        messages.success(request, 'El pedido de envío editado con exitó.')
        return redirect('orders:create-client')

    return render(request, template, context={
        'detail_obj': detail_obj,
        'info_form': info_form,
        'origin_form': origin_form,
        'destiny_form': destiny_form,
        'my_addressess_list': my_addressess_list
    })

class DeleteDetailView(LoginRequiredMixin, DeleteView):
    template_name = 'details/delete.html'

    def get_success_url(self) -> str:
        messages.success(self.request, "El pedido de envío eliminado con exitó")
        return self.request.GET.get('next', reverse('orders:create-client'))

    def get_queryset(self):
        return Detail.objects.all()