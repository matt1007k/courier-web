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