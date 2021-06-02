from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .utils import get_date_now, get_title_now
from orders.utils import get_total_orders_now

@login_required()
def dashboard(request):
    context = {
        'title': 'Dashboard',
        'now_summary': {
            'title': get_title_now(request),
            'date_now': get_date_now(),
            'total': get_total_orders_now(request) 
        }
    }
    return render(request, 'admin/dashboard.html', context=context)
