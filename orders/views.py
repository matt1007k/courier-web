import json
import ast
from details.paginations import LargeResultsSetPagination
from details.serializers import UnAssignOrignAddressSerializer
from django.http.response import HttpResponse, JsonResponse
from django.core.serializers import serialize
from rest_framework.generics import ListAPIView
from orders.mails import Mail
from clients.models import Client
from drivers.models import Driver
from typing import Any, Dict
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from datetime import datetime
from details.models import AssignDeliveryAddress, AssignOriginAddress, Detail, UnassignDeliveryAddress, UnassignOriginAddress

from django.views.generic import ListView, DetailView, detail

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .utils import delete_order, get_generate_tracking_code, get_or_create_order
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
        context['status'] = self.query_status() or Order.OrderStatus.REGISTERED
        self.request.session['order_id'] = None
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
            object_list = self.request.user.client.order_set.filter(status=self.query_status() or Order.OrderStatus.REGISTERED).order_by('-id')
        elif self.request.user.is_driver:
            object_list = self.request.user.driver.assignorder_set
        else:
            object_list = self.model.objects.filter(status=self.query_status() or Order.OrderStatus.REGISTERED).order_by('-id')
        
        return object_list

class AssignOriginAddressListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'details.view_assignoriginaddress'
    template_name = 'orders/assign/origins.html'
    paginate_by = 10
    model = AssignOriginAddress

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Recojo de paquetes'
        return context

    def query(self):
        return self.request.GET.get('q')

    def query_date(self):
        return self.request.GET.get('date')

    def query_status(self):
        return self.request.GET.get('status')

    def get_queryset(self):
        if self.request.user.is_driver:
            # object_list = self.request.user.driver.order_set.filter(status=self.query_status() or Order.OrderStatus.REGISTERED).order_by('-id')
            object_list = self.request.user.driver.assignoriginaddress_set.all().order_by('-id')
        return object_list

class AssignDeliveryAddressListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'details.view_assigndeliveryaddress'
    template_name = 'orders/assign/deliveries.html'
    paginate_by = 10
    model = AssignDeliveryAddress

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Entrega de paquetes'
        return context

    def query(self):
        return self.request.GET.get('q')

    def query_date(self):
        return self.request.GET.get('date')

    def query_status(self):
        return self.request.GET.get('status')

    def get_queryset(self):
        if self.request.user.is_driver:
            # object_list = self.request.user.driver.order_set.filter(status=self.query_status() or Order.OrderStatus.REGISTERED).order_by('-id')
            object_list = self.request.user.driver.assigndeliveryaddress_set.all().order_by('-id')
        return object_list

class UnassignOriginAddressListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'details.view_unassignoriginaddress'
    template_name = 'orders/assign/unassign-origins.html'
    paginate_by = 10
    model = UnassignOriginAddress

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Asignar recojos'
        return context

    def query(self):
        return self.request.GET.get('q')

    def get_queryset(self):
        object_list = self.model.objects.all().order_by('-id')
        return object_list

class UnassignDeliveryAddressListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'details.view_unassigndeliveryaddress'
    template_name = 'orders/assign/unassign-deliveries.html'
    paginate_by = 10
    model = UnassignDeliveryAddress

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Asignar entregas'
        return context

    def query(self):
        return self.request.GET.get('q')

    def get_queryset(self):
        object_list = self.model.objects.all().order_by('-id')
        return object_list

@login_required()
@permission_required('orders.add_order', login_url='/orders')
def create_order_view(request):
    order = get_or_create_order(request) 
        
    return render(request, 'orders/create.html', context={
        'order': order,
        'title': 'Registrar pedido'
    })

@login_required()
@permission_required('orders.view_order', login_url='/orders')
def cancel_order_view(request):
    if request.method == 'GET':
        delete_order(request) 
        return redirect('orders:index')

    messages.error(request, 'Error al cancelar el pedido')
    return redirect('orders:index')

@login_required()
# @permission_required('details.view_detail', login_url='/orders')
def add_addresses_view(request):
    template_name = 'orders/add-addresses.html'
    order = get_or_create_order(request)

    return render(request, template_name, context={
        'order': order,
        'title': 'Pedido - Direcciones de envío'
    })

@login_required()
@permission_required('orders.add_order', login_url='/orders')
def payment_view(request):
    template_name = 'orders/payment.html'
    order = get_or_create_order(request)
    if request.method == 'POST':
        if 'payed_image' in request.FILES and order.total > 0:
            if order.detail_set.count() == 0:
                messages.error(request, 'El pedido no tiene ninguna dirección de envío')
            order.payed_order(
                payed_image = request.FILES['payed_image'],
                tracking_code = get_generate_tracking_code(),
                type_ticket = request.POST.get('type_ticket')
            )
            for detail in order.detail_set.all():
                # Mail.send_origin_complete_order(detail, detail.address_origin.email)
                UnassignOriginAddress.objects.create(detail=detail)
            return redirect('orders:payment-success') 
        else:
            messages.error(request, 'Usted no ha realizado el pago, siga la forma de pago')

    return render(request, template_name, context={
        'order': order,
        'title': 'Pedido - Realizar pago'
    })

@login_required()
@permission_required('orders.add_order', login_url='/orders')
def payment_success_view(request):
    template_name = 'orders/payment-success.html'
    order = get_or_create_order(request)
    return render(request, template_name, context={
        'order': order
    })

def tracking_order_view(request):
    if request.method == 'GET':
        tracking_code = request.GET.get('tracking_code')
        order = Order.objects.filter(tracking_code=tracking_code).first()
        if order is None:
            return JsonResponse({
                'status': False,
            }, status=404)
        post_json = serialize('json', [order])
        detail_list = [{ 
                'address_origin_full_name': detail.address_origin.full_name, 
                'address_origin_cell_phone': detail.address_origin.cell_phone, 
                'address_origin_text': detail.address_origin.address_complete(), 
                'address_origin_reference': detail.address_origin.reference, 
                'address_origin_position': json.loads(detail.address_origin.address_gps), 
                'address_destiny_full_name': detail.address_destiny.full_name, 
                'address_destiny_cell_phone': detail.address_destiny.cell_phone, 
                'address_destiny_text': detail.address_destiny.address_complete(), 
                'address_destiny_reference': detail.address_destiny.reference, 
                'address_destiny_position': json.loads(detail.address_destiny.address_gps), 
            } for detail in order.detail_set.all()]
        order_json = json.dumps({
            'status': True,
            'order': json.loads(post_json)[0],
            'details': json.loads(json.dumps(detail_list))
        })
        return HttpResponse(order_json, content_type="application/json")

class DetailOrderView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = 'orders/detail.html'
    model = Order 
    permission_required = 'orders.view_order'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles del pedido'
        return context

@login_required()
def get_client_view(request):
    qs = get_or_create_order(request).client
    data = serialize('json', [qs])
    return HttpResponse(data, content_type="aplication/json")

@login_required()
def get_client_view(request):
    qs = get_or_create_order(request).client
    data = serialize('json', [qs])
    return HttpResponse(data, content_type="aplication/json")


class UnassignOriginAddressListAPIView(ListAPIView):
    queryset = UnassignOriginAddress.objects.all()
    serializer_class = UnAssignOrignAddressSerializer
    pagination_class = LargeResultsSetPagination 

@login_required()
@permission_required('details.add_assignoriginaddress', raise_exception=True)
def assign_origins_to_driver_view(request):
    if request.method == 'POST':
        detail_ids = ast.literal_eval(request.POST.get('assign_addresses_ids'))
        driver = Driver.objects.get(pk=request.POST.get('driver_id'))
        for id in detail_ids:
            detail = Detail.objects.get(pk=id)
            AssignOriginAddress.objects.create(
                detail=detail,
                driver=driver,
                admin=request.user if request.user.is_administrator else None
            )
            UnassignOriginAddress.objects.filter(detail=detail).first().delete()
        messages.success(request, 'Direccion(es) de recojo asignada(s) con éxito')
        return redirect("orders:unassign-origins")

@login_required()
@permission_required('details.add_assigndeliveryaddress', raise_exception=True)
def assign_deliveries_to_driver_view(request):
    if request.method == 'POST':
        detail_ids = ast.literal_eval(request.POST.get('assign_addresses_ids'))
        driver = Driver.objects.get(pk=request.POST.get('driver_id'))
        for id in detail_ids:
            detail = Detail.objects.get(pk=id)
            AssignDeliveryAddress.objects.create(
                detail=detail,
                driver=driver,
                admin=request.user if request.user.is_administrator else None
            )
            UnassignDeliveryAddress.objects.filter(detail=detail).first().delete()
        messages.success(request, 'Direccion(es) de entrega asignada(s) con éxito')
        return redirect("orders:unassign-deliveries")

