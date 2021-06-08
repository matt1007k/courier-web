from django.urls import reverse
from django.conf import settings

static_url = settings.STATIC_URL

def menu_items(request):
    menu_list = [
        {
            'title': 'Mi tienda' if request.user.is_authenticated and request.user.is_client else 'Dashboard',
            'icon': 'bx-line-chart',
            'img': None,
            'path': reverse('dash'),
            'permission': None,
        },
        {
            'title': 'Pedidos',
            'icon': None,
            'img': '{}icon/order-icon.svg'.format(static_url),
            'path': reverse('orders:index'),
            'permission': request.user.has_perm('orders.view_order'),
        },
        {
            'title': 'Motorizados',
            'icon': 'bx-user-check',
            'img': None,
            'path': reverse('drivers:index'),
            'permission': request.user.has_perm('drivers.view_driver'),
        },
        {
            'title': 'Mis pagos' if request.user.is_authenticated and request.user.is_driver else 'Pagos',
            'icon': 'bx-credit-card',
            'img': None,
            'path': reverse('driver_payments:index'),
            'permission': request.user.is_authenticated and request.user.is_driver or request.user.has_perm('driver_payments.view_driverpayment'),
        },
        {
            'title': 'Clientes',
            'icon': 'bx-user-pin',
            'img': None,
            'path': reverse('clients:index'),
            'permission': request.user.has_perm('clients.view_client'),
        },
        {
            'title': 'Direcciones',
            'icon': 'bx-current-location',
            'img': None,
            'path': reverse('addresses:index'),
            'permission': request.user.has_perm('addresses.view_address'),
        },
        {
            'title': 'Asignar recojos',
            'icon': 'bx-archive-in',
            'img': None,
            'path': reverse('orders:unassign-origins'),
            'permission': request.user.has_perm('details.view_unassignoriginaddress') and request.user.is_administrator,
        },
        {
            'title': 'Asignar entregas',
            'icon': 'bx-archive-out',
            'img': None,
            'path': reverse('orders:unassign-deliveries'),
            'permission': request.user.has_perm('details.view_unassigndeliveryaddress') and request.user.is_administrator,
        },
        {
            'title': 'Recojo de pedidos',
            'icon': 'bxs-direction-left',
            'img': None,
            'path': reverse('orders:origins'),
            'permission': request.user.has_perm('details.view_assignoriginaddress') and not request.user.is_client,
        },
        {
            'title': 'Entrega de pedidos',
            'icon': 'bx-cycling',
            'img': None,
            'path': reverse('orders:deliveries'),
            'permission': request.user.has_perm('details.view_assigndeliveryaddress') and not request.user.is_client,
        },
        # {
        #     'title': 'Reporte',
        #     'icon': 'bx-library',
        #     'img': None,
        #     'path': '#',
        #     'permission': None,
        # },
    ]
    return { 
        'menu_list': menu_list
    }