from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django.urls import reverse 

# import simplejson as json
# import json
from django.core.serializers.json import DjangoJSONEncoder

from .models import Detail
from addresses.models import Address

from .forms import DetailForm
from addresses.forms import OriginAddressForm, DestinyAddressForm

from orders.utils import get_or_create_order

def create_client_view(request):
    template = 'details/create-client.html'
    info_form = DetailForm(request.POST or None)
    origin_form = OriginAddressForm(request.POST or None)
    destiny_form = DestinyAddressForm(request.POST or None)
    client = request.user.client 
    my_addressess_list = Address.objects.filter(client=client).order_by('-id')
    if request.method == 'POST' and info_form.is_valid() and origin_form.is_valid()  and destiny_form.is_valid():
        order = get_or_create_order(request)
        origin_address = origin_form.cleaned_data['origin_address']
        origin_district = origin_form.cleaned_data['origin_district']
        origin_city = origin_form.cleaned_data['origin_city']
        origin_reference = origin_form.cleaned_data['origin_reference']

        destiny_address = destiny_form.cleaned_data['destiny_address']
        destiny_district = destiny_form.cleaned_data['destiny_district']
        destiny_city = destiny_form.cleaned_data['destiny_city']
        destiny_reference = destiny_form.cleaned_data['destiny_reference']

        address_origin = Address.objects.update_or_create(
            client = client,
            address = origin_address,
            district = origin_district,
            city = origin_city,
            reference = origin_reference,
            )

        address_destiny = Address.objects.update_or_create(
                client = client,
                address = destiny_address,
                district = destiny_district,
                city = destiny_city,
                reference = destiny_reference,
            )
        detail = Detail.objects.create(
            order=order, 
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            email = request.POST.get('email'),
            cell_phone = request.POST.get('cell_phone'),
            image = request.FILES['image'] if 'image' in request.FILES else False,
            description = request.POST.get('description'),
            address_origin=address_origin[0],
            address_destiny=address_destiny[0]
        )
        if not detail is None:
            messages.success(request, 'El pedido de envío agregado con exitó.')
            return redirect('orders:create-client')


    return render(request, template, context={
        'info_form': info_form,
        'origin_form': origin_form,
        'destiny_form': destiny_form,
        'my_addressess_list': my_addressess_list,
        'my_addressess_list_json': list(my_addressess_list)
    })

class DeleteDetailView(LoginRequiredMixin, DeleteView):
    template_name = 'details/delete.html'

    def get_success_url(self) -> str:
        messages.success(self.request, "El pedido de envío eliminado con exitó")
        return self.request.GET.get('next', reverse('orders:create-client'))

    def get_queryset(self):
        return Detail.objects.all()