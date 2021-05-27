import json
import ast
import threading
from datetime import datetime

from django.template.loader import get_template
from xhtml2pdf import pisa
from courier_app.utils import link_callback

from django.urls import reverse_lazy
from details.paginations import LargeResultsSetPagination
from details.serializers import UnAssignOrignAddressSerializer
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize
from rest_framework.generics import ListAPIView
from orders.mails import Mail
from drivers.models import Driver
from typing import Any, Dict
from django.contrib import messages
from django.shortcuts import redirect, render
from details.models import AssignDeliveryAddress, AssignOriginAddress, Detail, TrackingOrder, UnassignDeliveryAddress, UnassignOriginAddress

from django.views.generic import ListView, DetailView, View

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .utils import delete_order, get_or_create_order 
from pages.utils import is_valid_queryparams
from details.utils import get_generate_tracking_code
from .models import Order

class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'orders.view_order'
    template_name = 'orders/index.html'
    paginate_by = 10
    model = Detail

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pedidos'
        context['statuses'] = Detail.PackageStatus
        context['status'] = self.query_status() or Detail.PackageStatus.PENDING
        self.request.session['order_id'] = None
        return context

    def query(self):
        return self.request.GET.get('q')

    def query_date(self):
        return self.request.GET.get('date')

    def query_status(self):
        return self.request.GET.get('status')

    def query_origin(self):
        return self.request.GET.get('origin')

    def query_destiny(self):
        return self.request.GET.get('destiny')

    def get_queryset(self):
        if self.request.user.is_client:
            object_list = self.request.user.client.detail_set.exclude(tracking_code=None).filter(status=self.query_status() or Detail.PackageStatus.PENDING).order_by('-id')
        elif self.request.user.is_driver:
            clients = self.request.user.driver.get_clients()
            object_list = Detail.objects.none()
            for client in clients:
                object_list = object_list | client.detail_set.exclude(tracking_code=None).filter(status=self.query_status() or Detail.PackageStatus.PENDING).order_by('-id')
        else:
            object_list = self.model.objects.exclude(tracking_code=None).filter(status=self.query_status() or Detail.PackageStatus.PENDING).order_by('-id')
        
        if is_valid_queryparams(self.query_status()):
            object_list = object_list.filter(status=self.query_status())

        object_list = object_list.search_detail_and_client(self.query()).search_by_address_origin(self.query_origin()).search_by_address_delivery(self.query_destiny())

        if is_valid_queryparams(self.query_date()):
           object_list = object_list.filter(created_at__date=self.query_date()) 

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

    def query_driver(self):
        return self.request.GET.get('driver')

    def query_date_from(self):
        return self.request.GET.get('date_from')

    def query_date_to(self):
        return self.request.GET.get('date_to')

    def get_queryset(self):
        if self.request.user.is_driver:
            object_list = self.request.user.driver.assignoriginaddress_set.filter(detail__status=Detail.PackageStatus.PENDING).order_by('-id')
        else:
            object_list = self.model.objects.filter(detail__status=Detail.PackageStatus.PENDING).order_by('-created_at')

        object_list = object_list.search_driver(self.query_driver()).search_date_from(self.query_date_from()).search_date_to(self.query_date_to())
        return object_list

class ReporteAssignOriginAddressView(View):
    def query_driver(self):
        return self.request.GET.get('driver')

    def query_date_from(self):
        return self.request.GET.get('date_from')

    def query_date_to(self):
        return self.request.GET.get('date_to')

    def get(self, request, *args, **kwargs):
        try:
            template_name = 'orders/assign/report/origins.html'
            object_list = AssignOriginAddress.objects.filter(detail__status=Detail.PackageStatus.PENDING)
            origins = object_list.search_driver(self.query_driver()).search_date_from(self.query_date_from()).search_date_to(self.query_date_to())
            
            context={
                'filename': 'test',
                'date': datetime.now().date(),
                'logo': 'img/logo.png',
                'query': self.query_date_from(),
                'origins': origins
            }
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(context['filename'])
            template = get_template(template_name)
            html = template.render(context)

            pisa_status = pisa.CreatePDF(
                html, 
                dest=response,
                link_callback=link_callback
            )
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response

        except Exception as e:
            return e
        return HttpResponseRedirect(reverse_lazy('orders:origins'))


class AssignDeliveryAddressListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'details.view_assigndeliveryaddress'
    template_name = 'orders/assign/deliveries.html'
    paginate_by = 10
    model = AssignDeliveryAddress

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Entrega de paquetes'
        return context

    def query_driver(self):
        return self.request.GET.get('driver')

    def query_date_from(self):
        return self.request.GET.get('date_from')

    def query_date_to(self):
        return self.request.GET.get('date_to')

    def get_queryset(self):
        if self.request.user.is_driver:
            object_list = self.request.user.driver.assigndeliveryaddress_set.filter(detail__status=Detail.PackageStatus.PENDING).order_by('-created_at')
        else:
            object_list = self.model.objects.filter(detail__status=Detail.PackageStatus.PENDING).order_by('-created_at')

        object_list = object_list.search_driver(self.query_driver()).search_date_from(self.query_date_from()).search_date_to(self.query_date_to())
        return object_list

class ReporteAssignDeliveryAddressView(View):
    def query_driver(self):
        return self.request.GET.get('driver')

    def query_date_from(self):
        return self.request.GET.get('date_from')

    def query_date_to(self):
        return self.request.GET.get('date_to')

    def get(self, request, *args, **kwargs):
        try:
            template_name = 'orders/assign/report/deliveries.html'
            object_list = AssignDeliveryAddress.objects.filter(detail__status=Detail.PackageStatus.PENDING)
            deliveries = object_list.search_driver(self.query_driver()).search_date_from(self.query_date_from()).search_date_to(self.query_date_to())
            
            context={
                'filename': 'test',
                'date': datetime.now().date(),
                'logo': 'img/logo.png',
                'query': self.query_date_from(),
                'deliveries': deliveries
            }
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(context['filename'])
            template = get_template(template_name)
            html = template.render(context)

            pisa_status = pisa.CreatePDF(
                html, 
                dest=response,
                link_callback=link_callback
            )
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response

        except Exception as e:
            return e
        return HttpResponseRedirect(reverse_lazy('orders:origins'))

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
@permission_required('orders.add_order', raise_exception=True)
def create_order_view(request):
    order = get_or_create_order(request) 
        
    return render(request, 'orders/create.html', context={
        'order': order,
        'title': 'Registrar pedido'
    })

@login_required()
@permission_required('orders.view_order', raise_exception=True)
def cancel_order_view(request):
    if request.method == 'GET':
        delete_order(request) 
        return redirect('orders:index')

    messages.error(request, 'Error al cancelar el pedido')
    return redirect('orders:index')

@login_required()
# @permission_required('details.view_detail', raise_exception=True)
def add_addresses_view(request):
    template_name = 'orders/add-addresses.html'
    order = get_or_create_order(request)

    return render(request, template_name, context={
        'order': order,
        'title': 'Pedido - Direcciones de envío'
    })

@login_required()
@permission_required('orders.add_order', raise_exception=True)
def payment_view(request):
    template_name = 'orders/payment.html'
    order = get_or_create_order(request)
    if request.method == 'POST':
        if 'payed_image' in request.FILES and order.total > 0:
            if order.detail_set.count() == 0:
                messages.error(request, 'El pedido no tiene ninguna dirección de envío')
            order.payed_order(
                payed_image = request.FILES['payed_image'],
                type_ticket = request.POST.get('type_ticket'),
                business_name = request.POST.get('business_name'),
                ruc = request.POST.get('ruc'),
            )
            for detail in order.detail_set.all():
                detail.payed(
                    tracking_code = get_generate_tracking_code(),
                )
                # thread = threading.Thread(
                #     target=Mail.send_complete_order,
                #     args=(detail, detail.address_origin.email, request)
                # )
                # thread.start()
                # thread2 = threading.Thread(
                #     target=Mail.send_complete_order,
                #     args=(detail, detail.address_destiny.email, request)
                # )
                # thread2.start()
                # Mail.send_complete_order(detail, detail.address_destiny.email, request)
                TrackingOrder.objects.create(
                    detail=detail,
                    location='Pendiente a recojer en el dirección ingresada.'
                )
                if not detail.is_unassign_delivery:
                    UnassignDeliveryAddress.objects.create(detail=detail)
                if not detail.is_unassign_origin:
                    UnassignOriginAddress.objects.create(detail=detail)
            return redirect('orders:payment-success') 
        else:
            messages.error(request, 'Usted no ha realizado el pago, siga la forma de pago')

    return render(request, template_name, context={
        'order': order,
        'title': 'Pedido - Realizar pago'
    })

@login_required()
@permission_required('orders.add_order', raise_exception=True)
def payment_success_view(request):
    template_name = 'orders/payment-success.html'
    order = get_or_create_order(request)
    return render(request, template_name, context={
        'order': order
    })

def tracking_order_view(request):
    if request.method == 'GET':
        tracking_code = request.GET.get('tracking_code')
        detail = Detail.objects.filter(tracking_code=tracking_code).first()
        if detail is None:
            return JsonResponse({
                'status': False,
            }, status=404)
        detail_dict = { 
                'tracking_code': detail.tracking_code,
                'address_origin_full_name': detail.address_origin.full_name, 
                'address_origin_cell_phone': detail.address_origin.cell_phone, 
                'address_origin_text': detail.address_origin.address_complete(), 
                'address_origin_reference': detail.address_origin.reference, 
                'address_origin_position': detail.address_origin.address_gps, 
                'address_destiny_full_name': detail.address_destiny.full_name, 
                'address_destiny_cell_phone': detail.address_destiny.cell_phone, 
                'address_destiny_text': detail.address_destiny.address_complete(), 
                'address_destiny_reference': detail.address_destiny.reference, 
                'address_destiny_position': detail.address_destiny.address_gps,
                'status': detail.status,
                'status_label': detail.get_status_display(),
                'distance': str(detail.distance)
            }
        order_json = json.dumps({
            'status': True,
            'detail': detail_dict 
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
            if not detail.is_assign_origin:
                TrackingOrder.objects.create(
                    detail=detail,
                    location='Motorizado asignado para recojer el paquete'
                )
                AssignOriginAddress.objects.create(
                    detail=detail,
                    driver=driver,
                    admin=request.user if request.user.is_administrator else None
                )
                detail.pended()
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
            if not detail.is_assign_delivery:
                TrackingOrder.objects.create(
                    detail=detail,
                    location='Motorizado asignado para entregar el paquete'
                )
                AssignDeliveryAddress.objects.create(
                    detail=detail,
                    driver=driver,
                    admin=request.user if request.user.is_administrator else None
                )
                detail.pended()
                UnassignDeliveryAddress.objects.filter(detail=detail).first().delete()
        messages.success(request, 'Direccion(es) de entrega asignada(s) con éxito')
        return redirect("orders:unassign-deliveries")

@login_required()
@permission_required('details.add_unassignoriginaddress', raise_exception=True)
def return_unassign_origin_view(request, pk):
    if request.method == 'GET':
        detail = Detail.objects.get(pk=pk)
        if not detail.is_unassign_origin:
            TrackingOrder.objects.create(
                detail=detail,
                location='Se reprogramo el recojo del paquete'
            )
            detail.reprogrammed()
            UnassignOriginAddress.objects.create(
                detail=detail,
            )
            AssignOriginAddress.objects.filter(detail=detail).first().delete()
            messages.success(request, 'La dirección de recojo, dejó de ser asignada al motorizado.')
            return redirect("orders:origins")
        messages.success(request, 'La dirección de recojo, ya dejó de ser asignada previamente.')
        return redirect("orders:origins")

@login_required()
@permission_required('details.add_unassigndeliveryaddress', raise_exception=True)
def return_unassign_delivery_view(request, pk):
    if request.method == 'GET':
        detail = Detail.objects.get(pk=pk)
        if not detail.is_unassing_delivery:
            TrackingOrder.objects.create(
                detail=detail,
                location='Se reprogramo la entrega del paquete'
            )
            detail.reprogrammed()
            UnassignDeliveryAddress.objects.create(
                detail=detail,
            )
            AssignDeliveryAddress.objects.filter(detail=detail).first().delete()
            messages.success(request, 'La dirección de envío, dejó de ser asignada al motorizado.')
            return redirect("orders:deliveries")
        messages.success(request, 'La dirección de envío, ya dejó de ser asignada previamente.')
        return redirect("orders:deliveries")