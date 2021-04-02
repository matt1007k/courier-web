from drivers.models import Driver
from .models import Order

def get_or_create_order(request):
    user = request.user if request.user.is_authenticated else None
    order_id  = request.session.get('order_id')

    if order_id:
        order = Order.objects.get(pk=order_id)
    else:
        tracking_code = get_generate_tracking_code()
        
        order = Order.objects.create(
                                client=user.client, 
                                tracking_code=tracking_code
                                )
    request.session['order_id'] = order.id
    return order

def fields_origin_form(detail):
    fields = {
        'origin_address': detail.address_origin.address,
        'origin_district': detail.address_origin.district,
        'origin_city': detail.address_origin.city,
        'origin_reference': detail.address_origin.reference,
    }
    return fields

def fields_destiny_form(detail):
    fields = {
        'destiny_address': detail.address_destiny.address,
        'destiny_district': detail.address_destiny.district,
        'destiny_city': detail.address_destiny.city,
        'destiny_reference': detail.address_destiny.reference,
    }
    return fields

def get_generate_tracking_code():
    orders_count = Order.objects.count()
    zero = ''
    
    if orders_count < 10:
        zero = '00000'
    if orders_count >= 10:
        zero = '0000'
    if orders_count >= 100:
        zero = '000'
    if orders_count >= 1000:
        zero = '00'
    if orders_count >= 10000:
        zero = '0'
    if orders_count >= 100000:
        zero = ''

    code = '{}{}'.format(zero, orders_count + 1)
    return 'CC{}'.format(code)