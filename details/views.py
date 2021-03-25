from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django.urls import reverse 

from .models import Detail
from addresses.models import Address

from .forms import DetailForm
from addresses.forms import OriginAddressForm, DestinyAddressForm

from orders.utils import get_or_create_order

def create_client_view(request):
    template = 'details/create-client.html'
    info_form = DetailForm
    origin_form = OriginAddressForm
    destiny_form = DestinyAddressForm
    if request.method == 'POST':
        order = get_or_create_order(request)
        address_origin = Address.objects.create(
            client=request.user.client,
            address = request.POST.get('origin_address'),
            district = request.POST.get('origin_district'),
            city = request.POST.get('origin_city'),
            reference = request.POST.get('origin_reference'),
        )
        address_destiny = Address.objects.create(
            client=request.user.client,
            address = request.POST.get('destiny_address'),
            district = request.POST.get('destiny_district'),
            city = request.POST.get('destiny_city'),
            reference = request.POST.get('destiny_reference'),
        )
        detail = Detail.objects.create(
            order=order, 
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            email = request.POST.get('email'),
            cell_phone = request.POST.get('cell_phone'),
            image = request.FILES['image'],
            description = request.POST.get('description'),
            address_origin=address_origin,
            address_destiny=address_destiny
        )
        if not detail is None:
            messages.success(request, 'El pedido de envío agregado con exitó.')
            return redirect('orders:create-client')


    return render(request, template, context={
        'info_form': info_form,
        'origin_form': origin_form,
        'destiny_form': destiny_form,
    })

class DeleteDetailView(LoginRequiredMixin, DeleteView):
    template_name = 'details/delete.html'

    def get_success_url(self) -> str:
        messages.success(self.request, "El pedido de envío eliminado con exitó")
        return self.request.GET.get('next', reverse('orders:create-client'))

    def get_queryset(self):
        return Detail.objects.all()