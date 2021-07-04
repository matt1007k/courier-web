from io import BytesIO, StringIO
import json
import ast
import os
from settings.models import Setting
import threading
from datetime import datetime

from django.template.loader import get_template
from xhtml2pdf import pisa
from courier_app.utils import link_callback

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from details.paginations import LargeResultsSetPagination
from details.serializers import UnAssignOrignAddressSerializer
from django.http.response import FileResponse, HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize
from rest_framework.generics import ListAPIView, get_object_or_404
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
from details.utils import get_generate_tracking_code, get_time_now
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
        context['status'] = self.query_status() or None
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
            object_list = self.request.user.client.detail_set.exclude(tracking_code=None).order_by('-id')
        elif self.request.user.is_driver:
            clients = self.request.user.driver.get_clients()
            object_list = Detail.objects.none()
            for client in clients:
                object_list = object_list | client.detail_set.exclude(tracking_code=None).order_by('-id')
        else:
            object_list = self.model.objects.exclude(tracking_code=None).order_by('-id')
        
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
            object_list = self.request.user.driver.assignoriginaddress_set.exclude(is_received=True).order_by('-created_at')
        else:
            object_list = self.model.objects.order_by('-created_at')

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
            object_list = AssignOriginAddress.objects.exclude(is_received=True)
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
            object_list = self.request.user.driver.assigndeliveryaddress_set.exclude(is_delivered=True).order_by('-created_at')
        else:
            object_list = self.model.objects.order_by('-created_at')

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
            object_list = AssignDeliveryAddress.objects.exclude(is_delivered=True)
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
    if request.user.is_client:
        setting = Setting.objects.first() 
        if setting is None:
            messages.error(request, 'Falta una configuración, le recomedamos comunicarse con el administrador del sistema')
            return redirect('orders:index')

        if not get_time_now() >= setting.time_limit_to and (get_time_now() <= setting.time_limit_from or get_time_now() >= setting.time_limit_from):
            setting.cannot_create_order()
            messages.error(request, setting.message_origin)
            return redirect('orders:index')
        else:
            setting.can_create_order()

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
                if detail.tracking_code is None:
                    detail.payed(
                        tracking_code = get_generate_tracking_code(),
                    )
                if detail.tracking_code:
                    if detail.address_origin.email:
                        thread = threading.Thread(
                            target=Mail.send_complete_order,
                            args=(detail, detail.address_origin.full_name, detail.address_origin.email, request)
                        )
                        thread.start()
                    if detail.address_destiny.email:
                        thread2 = threading.Thread(
                            target=Mail.send_complete_order,
                            args=(detail, detail.address_destiny.full_name, detail.address_destiny.email, request)
                        )
                        thread2.start()
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

class ReportRotuladoView(View):
    def get(self, request, *args, **kwargs):
        request.session['order_id'] = None
        try:
            template_name = 'orders/report/rotulado.html'
            order = get_object_or_404(Order, pk=self.kwargs['pk']) 

            context={
                'filename': 'rotulado-{}'.format(order.pk),
                'date': datetime.now().date(),
                'logo': 'img/logo.png',
                'ui': 'img/report/ui-rotulado.png',
                'order': order,
            }
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(context['filename'])
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

def tracking_order_view(request):
    if request.method == 'GET':
        tracking_code = request.GET.get('tracking_code')
        detail = Detail.objects.filter(tracking_code=tracking_code).first()
        trackings = detail.trackings.all().order_by('created_at')
        if detail is None:
            return JsonResponse({
                'status': False,
            }, status=404)
        
        if trackings.count() > 0:
            trackings_dict = []
            for tracking in trackings:
                trackings_dict.append({
                    'created_at': tracking.created_at_localtime_localize(),
                    'location': tracking.location 
                }) 
        else:
            trackings_dict = []
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
            'detail': detail_dict,
            'trackings': trackings_dict
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
                    location='El motorizado ha sido asignado para recoger tu pedido'
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
                    location='El motorizado ha sido asignado para entregar tu pedido'
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
                location='Se reprogramo el recojo de tu paquete'
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
                location='Se reprogramo la entrega de tu paquete'
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


class ReportOrdersPDFView(View):
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

    def get(self, request, *args, **kwargs):
        try:
            template_name = 'orders/report/order-list.html'
            orders = Detail.objects.search_detail_and_client(self.query()).search_by_address_origin(self.query_origin()).search_by_address_delivery(self.query_destiny()).search_by_status(self.query_status()).search_by_date(self.query_date())
            date_now = datetime.now().strftime("%d-%m-%Y")

            context={
                'filename': 'reporte-ordenes-{}'.format(date_now),
                'date': date_now,
                'logo': 'img/logo.png',
                'ui': 'img/report/ui-rotulado.png',
                'orders': orders,
            }
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(context['filename'])
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
        return HttpResponseRedirect(reverse_lazy('orders:index'))

class ExportOrdersExcelView(View):
    pass
    # def query(self):
    #     return self.request.GET.get('q')

    # def query_date(self):
    #     return self.request.GET.get('date')

    # def query_status(self):
    #     return self.request.GET.get('status')

    # def query_origin(self):
    #     return self.request.GET.get('origin')

    # def query_destiny(self):
    #     return self.request.GET.get('destiny')

    # def get(self, request, *args, **kwargs):
    #     # try:
    #     date_now = datetime.now().strftime("%d-%m-%Y")
    #     filename = 'reporte-ordenes-{}'.format(date_now),

    #     response = HttpResponse(content_type='application/vnd.ms-excel')
    #     # response['Content-Disposition'] = 'attachment; filename={}.xls'.format(filename)

    #     wb = xlwt.Workbook(encoding='utf-8')
    #     ws = wb.add_sheet('Ordenes')
    #     row_num = 0
    #     font_style = xlwt.XFStyle()
    #     font_style.font.bold = True

    #     headers = ['# Tracking', 'Cliente', 'Fecha', 'Dirección', 'Quien atenderá', 'Celular', 'Precio']
    #     for col_num in range(len(headers)):
    #         ws.write(row_num, col_num, headers[col_num], font_style)

    #     font_style = xlwt.XFStyle()

    #     columns = ['tracking_code', 'client__first_name', 'created_at', 'address_destiny__address', 'address_destiny__full_name', 'address_destiny__cell_phone', 'price_rate']
    #     # rows = Detail.objects.search_detail_and_client(self.query()).search_by_address_origin(self.query_origin()).search_by_address_delivery(self.query_destiny()).search_by_status(self.query_status()).search_by_date(self.query_date())
    #     rows = Detail.objects.all().order_by('-id')

    #     for detail in rows:
    #         row_num += 1
    #         ws.write(row_num, 0, detail.tracking_code, font_style)
    #         ws.write(row_num, 1, detail.client.full_name(), font_style)
    #         ws.write(row_num, 2, detail.created_at_localtime_localize(), font_style)
    #         ws.write(row_num, 3, detail.address_destiny.address_complete(), font_style)
    #         ws.write(row_num, 4, detail.address_destiny.full_name, font_style)
    #         ws.write(row_num, 5, detail.address_destiny.cell_phone, font_style)
    #         ws.write(row_num, 6, detail.price_rate, font_style)

    #     # output = StringIO()
    #     output = BytesIO()
    #     wb.save(output)

    #     output.seek(0)
    #     response["Content-Disposition"] = "attachment;filename*=utf-8''{}".format(filename)

    #     response.write(output.getValue())

            # for i, h in enumerate(headers):
            #     ws.write(0, i, h, font_style)
            # cols = 1
            # for query in rows.values(*columns):
            #     for i, k in enumerate(columns):
            #         v = query.get(k)
            #         if isinstance(v, datetime):
            #             v = v.strftime('%Y-%m-%d %H:%M:%S')
            #         ws.write(cols, i, v)
            #     cols += 1
            # wb.save(filename)
            # response = FileResponse(file_iterator(filename))
            # response['Content-Type'] = 'application/vnd.ms-excel'
            # response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)

            # wb.save(response)
        # wb.save(response)
        # return response

        # except Exception as e:
        #     return e



def export_orders_excel_view(request):
    return HttpResponse({
        'status': True
    })
    # query = request.GET.get('q')
    # query_date = request.GET.get('date')
    # query_status = request.GET.get('status')
    # query_origin = request.GET.get('origin')
    # query_destiny = request.GET.get('destiny')

    # date_now = datetime.now().strftime("%d-%m-%Y")
    # filename = 'reporte-ordenes-{}'.format(date_now),

    # response = HttpResponse(content_type='application/vnd.ms-excel')
    # response['Content-Disposition'] = 'attachment; filename={}.xls'.format(filename)

    # wb = xlwt.Workbook(encoding='utf-8')
    # ws = wb.add_sheet(u'Ordenes')
    # row_num = 0
    # font_style = xlwt.XFStyle()
    # font_style.font.bold = True

    # columns = ['# Tracking', 'Cliente', 'Fecha', 'Dirección', 'Quien atenderá', 'Celular', 'Precio']
    # for col_num in range(len(columns)):
    #     ws.write(row_num, col_num, columns[col_num], font_style)

    # font_style = xlwt.XFStyle()

    # rows = Detail.objects.search_detail_and_client(query).search_by_address_origin(query_origin).search_by_address_delivery(query_destiny).search_by_status(query_status).search_by_date(query_date).values_list('tracking_code', 'client__first_name', 'created_at', 'address_destiny__address', 'address_destiny__full_name', 'address_destiny__cell_phone', str('price_rate'))

    # for row in rows:
    #     row_num += 1

    #     for col_num in range(len(row)):
    #         ws.write(row_num, col_num, str(row[col_num]), font_style)

    # wb.save(response)
    # return response



