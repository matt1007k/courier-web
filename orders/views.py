from typing import Any, Dict
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from datetime import datetime

from django.views.generic import ListView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .utils import get_or_create_order
from .models import Order

class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'orders/index.html'
    paginate_by = 10
    model = Order

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pedidos'
        context['statuses'] = Order.OrderStatus
        context['status'] = self.query_status() or Order.OrderStatus.PENDING
        return context

    def query(self):
        return self.request.GET.get('q')

    def query_date(self):
        return self.request.GET.get('date')

    def query_status(self):
        return self.request.GET.get('status')

    def get_queryset(self):
        if self.query() and self.query_date():            
            filters = Q(tracking_code__icontains=self.query()) | Q(client__first_name__icontains=self.query()) | Q(client__last_name__icontains=self.query()) | Q(created_at__date=self.query_date())
            
            print('date: ',   self.query_date())
            object_list = self.model.objects.filter(filters)
        elif self.query_date() and self.query_status():
            object_list = self.model.objects.filter(status=self.query_status() or Order.OrderStatus.PENDING, created_at__date=self.query_date()).order_by('-id')
        else:
            object_list = self.model.objects.filter(status=self.query_status() or Order.OrderStatus.PENDING).order_by('-id')
            # created_at__date='2021-3-25'
            # created_at__range=(start_date, end_date)
        return object_list

@login_required()
def create_order_client_view(request):
    order = get_or_create_order(request) 
    if request.method == 'POST':
        if 'image_payed' in request.FILES:
            if order.detail_set.count() == 0:
                messages.error(request, 'El pedido no tiene ningún elemento de envió')
            image_payed = request.FILES['image_payed']
            order.image_payed = image_payed
            order.save()
            messages.success(request, 'El pedido se ha realizado con exitó')
            # return redirect('orders:index') 
        else:
            messages.error(request, 'Usted no ha realizado el pago, siga la forma de pago')
        
    return render(request, 'orders/create-client.html', context={
        'order': order
    })

@login_required()
def create_order_view(request):
    order = get_or_create_order(request) 
    if request.method == 'POST':
        if 'image_payed' in request.FILES:
            if order.detail_set.count() == 0:
                messages.error(request, 'El pedido no tiene ningún elemento de envió')
            image_payed = request.FILES['image_payed']
            order.image_payed = image_payed
            order.save()
            messages.success(request, 'El pedido se ha realizado con exitó')
            # return redirect('orders:index') 
        else:
            messages.error(request, 'Usted no ha realizado el pago, siga la forma de pago')
        
    return render(request, 'orders/create-client.html', context={
        'order': order
    })