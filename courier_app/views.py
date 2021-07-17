from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from .utils import get_date_now, get_title_now
from orders.utils import get_count_orders_now, get_summary_count, get_total_orders_now, get_list_right
from orders.models import Order
from driver_payments.models import DriverPayment
from details.models import Detail

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

@login_required()
@permission_required('service_prices.view_budget', raise_exception=True)
def budget_view(request):
    template_name = 'service_prices/budgets.html'
    total_payment = sum([payment.total for payment in DriverPayment.objects.all()])
    total_entry = sum([order.total for order in Order.objects.exclude(payed_image=None)])
    total = total_entry - total_payment
    percent = round(total_payment / total_entry, 2) * 100
    entries = Detail.objects.all().order_by('-id')[:5]
    expenses = DriverPayment.objects.all().order_by('-id')[:5]

    return render(request, template_name, context={
        'title': 'Presupuesto',
        'total': int(total),
        'total_payment': int(total_payment),
        'total_entry': int(total_entry),
        'percent': percent,
        'entries': entries,
        'expenses': expenses,
    })
