from django.db.models.signals import pre_init
from clients.models import Client
from typing import Any, Dict
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from datetime import datetime

from django.views.generic import ListView

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .utils import delete_order, get_or_create_order
from .models import Order

class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'orders.view_order'
    template_name = 'orders/index.html'
    paginate_by = 10
    model = Order

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pedidos'
        context['statuses'] = Order.OrderStatus
        context['client_list'] = Client.objects.all()[:5]
        context['status'] = self.query_status() or Order.OrderStatus.PENDING
        delete_order(self.request)
        return context

    def query(self):
        return self.request.GET.get('q')

    def query_date(self):
        return self.request.GET.get('date')

    def query_status(self):
        return self.request.GET.get('status')

    def get_queryset(self):
        # if self.query() and self.query_date():            
        #     filters = Q(tracking_code__icontains=self.query()) | Q(client__first_name__icontains=self.query()) | Q(client__last_name__icontains=self.query()) | Q(created_at__date=self.query_date())
            
        #     object_list = self.model.objects.filter(client=client).filter(filters)
        # elif self.query_date() and self.query_status():
        #     object_list = self.model.objects.filter(client=client).filter(status=self.query_status() or Order.OrderStatus.PENDING, created_at__date=self.query_date()).order_by('-id')
        # else:
        #     object_list = self.model.objects.filter(client=client).filter(status=self.query_status() or Order.OrderStatus.PENDING).order_by('-id')
            # created_at__date='2021-3-25'
            # created_at__range=(start_date, end_date)
        if self.request.user.is_client:
            object_list = self.request.user.client.order_set.filter(status=self.query_status() or Order.OrderStatus.PENDING).order_by('-id')
        elif self.request.user.is_driver:
            object_list = self.request.user.driver.order_set.filter(status=self.query_status() or Order.OrderStatus.PENDING).order_by('-id')
            print(self.request.user.driver.order_set.count())
        else:
            object_list = self.model.objects.filter(status=self.query_status() or Order.OrderStatus.PENDING).order_by('-id')
        
        return object_list

@login_required()
@permission_required('orders.add_order', login_url='/orders')
def create_order_client_view(request):
    order = get_or_create_order(request) 
    if request.method == 'POST':
        if 'image_payed' in request.FILES:
            if order.detail_set.count() == 0:
                messages.error(request, 'El pedido no tiene ningún elemento de envió')
            image_payed = request.FILES['image_payed']
            order.image_payed = image_payed
            order.save()
            messages.success(request, 'El pedido se ha realizado con éxito')
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
            messages.success(request, 'El pedido se ha realizado con éxito')
            # return redirect('orders:index') 
        else:
            messages.error(request, 'Usted no ha realizado el pago, siga la forma de pago')
        
    return render(request, 'orders/create.html', context={
        'order': order
    })

@login_required()
def cancel_order_view(request):
    if request.method == 'GET':
        delete_order(request) 
        return redirect('orders:index')

    messages.error(request, 'Error al cancelar el pedido')
    return redirect('orders:index')

@login_required()
def add_addresses_view(request):
    template_name = 'orders/add-addresses.html'
    order = get_or_create_order(request)

    return render(request, template_name, context={
        'order': order
    })