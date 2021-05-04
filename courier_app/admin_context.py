from django.urls import reverse
from django.conf import settings

static_url = settings.STATIC_URL

def menu_items(request):
    menu_list = [
        {
            'title': 'Dashboard',
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
            'icon': 'bxs-direction-right',
            'img': None,
            'path': reverse('orders:unassign-origins'),
            'permission': request.user.has_perm('details.view_unassignoriginaddress') and request.user.is_administrator,
        },
        {
            'title': 'Asignar entregas',
            'icon': 'bx-cycling',
            'img': None,
            'path': reverse('orders:unassign-deliveries'),
            'permission': request.user.has_perm('details.view_unassigndeliveryaddress') and request.user.is_administrator,
        },
        {
            'title': 'Recojo de pedidos',
            'icon': 'bxs-direction-right',
            'img': None,
            'path': reverse('orders:origins'),
            'permission': request.user.has_perm('details.view_assignoriginaddress') and request.user.is_driver,
        },
        {
            'title': 'Entrega de pedidos',
            'icon': 'bx-cycling',
            'img': None,
            'path': reverse('orders:deliveries'),
            'permission': request.user.has_perm('details.view_assigndeliveryaddress') and request.user.is_driver,
        },
        {
            'title': 'Reporte',
            'icon': 'bx-library',
            'img': None,
            'path': '#',
            'permission': None,
        },
    ]
    return { 
        'menu_list': menu_list
    }