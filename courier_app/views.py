from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .utils import get_date_now, get_title_now
from orders.utils import get_count_orders_now, get_summary_count, get_total_orders_now, get_list_right

@login_required()
def dashboard(request):
    context = {
        'title': 'Mi tienda' if request.user.is_authenticated and request.user.is_client else 'Dashboard',
        'now_summary': {
            'title': get_title_now(request),
            'date_now': get_date_now(),
            'total': get_total_orders_now(request),
            'count': get_count_orders_now(request),
            'title_order': 'Pedidos realizados' if request.user.is_authenticated and request.user.is_client else 'Pedidos'
        },
        'summary_count': get_summary_count(request),
        'list_right': get_list_right(request)
    }
    return render(request, 'admin/dashboard.html', context=context)
