from .models import Order
from clients.models import Client

def get_or_create_order(request):
    user = request.user if request.user.is_authenticated else None
    order_id  = request.session.get('order_id')

    if order_id:
        order = Order.objects.get(pk=order_id)
    else:
        if user.is_client:
            client = user.client
        else:
            client = Client.objects.get(pk=request.POST.get('client_id'))
        order = Order.objects.create(
                                client=client, 
                                )
    request.session['order_id'] = order.id
    return order

def delete_order(request):
    order_id = request.session.get('order_id')
    if order_id:
        Order.objects.get(pk=order_id).delete()
        # order = Order.objects.get(pk=order_id)
        # order.canceled()
        request.session['order_id'] = None
        
def fields_origin_form(detail):
    fields = {
        'origin_full_name': detail.address_origin.full_name,
        'origin_email': detail.address_origin.email,
        'origin_cell_phone': detail.address_origin.cell_phone,
        'origin_address': detail.address_origin.address,
        'origin_district': detail.address_origin.district,
        'origin_city': detail.address_origin.city,
        'origin_reference': detail.address_origin.reference,
        'origin_position': detail.address_origin.address_gps,
        'origin_address_detail': detail.address_origin.address_detail
    }
    return fields

def fields_destiny_form(detail):
    fields = {
        'destiny_full_name': detail.address_destiny.full_name,
        'destiny_email': detail.address_destiny.email,
        'destiny_cell_phone': detail.address_destiny.cell_phone,
        'destiny_address': detail.address_destiny.address,
        'destiny_district': detail.address_destiny.district,
        'destiny_city': detail.address_destiny.city,
        'destiny_reference': detail.address_destiny.reference,
        'destiny_address_detail': detail.address_destiny.address_detail,
        'destiny_position': detail.address_destiny.address_gps,
        'price_rate': detail.price_rate,
        'distance': detail.distance,
    }
    return fields
