from .models import Order

def generate_tracking_code(request):
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

    code = '{}{}'.format(zero, orders_count)
    return 'CC{}'.format(code)