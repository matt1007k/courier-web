from datetime import datetime
from drivers.models import Driver
from .models import Order
from clients.models import Client
from details.models import AssignOriginAddress, Detail
from django.urls import reverse
from django.conf import settings

static_url = settings.STATIC_URL

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


def get_total_orders_now(request):
    if request.user.is_driver:
        total = request.user.driver.get_total_payment_today()
    else:
        total = sum([order.total for order in Order.objects.filter(created_at__gte=datetime.now().strftime('%Y-%m-%d'))])
    return round(total, 0)
    
def get_count_orders_now(request):
    if request.user.is_driver:
        count = request.user.driver.get_count_orders_today()
    elif request.user.is_client:
        count = request.user.client.detail_set.filter(created_at__gte=datetime.now().strftime('%Y-%m-%d')).count()
    else:
        count = Detail.objects.filter(created_at__gte=datetime.now().strftime('%Y-%m-%d')).count()
    return count

def get_summary_count(request):
    data = {
        'driver_title1': 'Pedidos entregados',
        'driver_icon1': '{}icon/order-icon.svg'.format(static_url),
        'driver_count1': request.user.driver.get_orders_delivery_address().count() if request.user.is_authenticated and request.user.is_driver else '0',
        'driver_more_path1': reverse('orders:deliveries'),
        'driver_title2': 'Clientes asociados',
        'driver_icon2': 'bx-user-pin',
        'driver_count2': request.user.driver.clients_count() if request.user.is_authenticated and request.user.is_driver else '0',
        'driver_more_path2': '',
        'driver_title3': 'Pagos recibidos',
        'driver_icon3': 'bx-credit-card',
        'driver_count3': 'S/ {}'.format(request.user.driver.get_total_payments()) if request.user.is_authenticated and request.user.is_driver else 'S/ 0',
        'driver_more_path3': '#',

        'client_title1': 'Pedidos realizados',
        'client_icon1': '{}icon/order-icon.svg'.format(static_url),
        'client_count1': request.user.client.detail_set.count() if request.user.is_authenticated and request.user.is_client else '0',
        'client_more_path1': reverse('orders:index'),
        'client_title2': 'Direcciones',
        'client_icon2': 'bx-current-location',
        'client_count2': request.user.client.address_set.count() if request.user.is_authenticated and request.user.is_client else '0',
        'client_more_path2': reverse('addresses:index'),

        'admin_title1': 'Pedidos',
        'admin_icon1': '{}icon/order-icon.svg'.format(static_url),
        'admin_count1': Detail.objects.count(),
        'admin_more_path1': reverse('orders:index'),
        'admin_title2': 'Clientes',
        'admin_icon2': 'bx-user-pin',
        'admin_count2': Client.objects.count(),
        'admin_more_path2': reverse('clients:index'),
        'admin_title3': 'Motorizados',
        'admin_icon3': 'bx-user-check',
        'admin_count3': Driver.objects.count(),
        'admin_more_path3': reverse('drivers:index'),
    }

    return data

def get_list_right(request):
    data = {
        'driver_title': 'Pedidos a recojer',
        'driver_description': 'Los últimos pedidos a recojer',
        'driver_origins': request.user.driver.get_last_orders_origin_address(5) if request.user.is_driver else None,
        'driver_more_path': reverse('orders:origins'),
        'client_title': 'Mis últimas direcciones',
        'client_description': 'Las últimas direcciones registradas',
        'client_addresses': request.user.client.get_last_addresses(5) if request.user.is_client else None,
        'client_more_path': reverse('addresses:index'),
        'admin_title': 'Últimos clientes',
        'admin_description': 'Los últimos clientes registrados',
        'admin_clients': Client.objects.all().order_by('-id')[:5],
        'admin_more_path': reverse('clients:index')
    }

    return data