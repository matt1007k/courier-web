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
            'img': '{}img/icon/order-icon.svg'.format(static_url),
            'path': reverse('orders:index'),
            'permission': request.user.has_perm('orders.view_order'),
        }
    ]
    return { 
        'menu_list': menu_list
    }