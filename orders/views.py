from io import BytesIO
import pandas as pd
import json
import ast
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
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
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
from details.utils import get_generate_tracking_code, get_time_now, time_in_range
from .models import Order

@login_required()
@permission_required('orders.view_order', raise_exception=True)
def index(request):
    template_name = 'orders/index.html'
    title = "Pedidos"
    return render(request, template_name, context={
        'title': title
    })

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
            object_list = self.request.user.driver.assignoriginaddress_set.exclude(
                is_received=True).order_by('-created_at')
        else:
            object_list = self.model.objects.order_by('-created_at')

        object_list = object_list.search_driver(self.query_driver()).search_date_from(
            self.query_date_from()).search_date_to(self.query_date_to())
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
            origins = object_list.search_driver(self.query_driver()).search_date_from(
                self.query_date_from()).search_date_to(self.query_date_to())

            context = {
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
            object_list = self.request.user.driver.assigndeliveryaddress_set.exclude(
                is_delivered=True).order_by('-created_at')
        else:
            object_list = self.model.objects.order_by('-created_at')

        object_list = object_list.search_driver(self.query_driver()).search_date_from(
            self.query_date_from()).search_date_to(self.query_date_to())
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
            object_list = AssignDeliveryAddress.objects.exclude(
                is_delivered=True)
            deliveries = object_list.search_driver(self.query_driver()).search_date_from(
                self.query_date_from()).search_date_to(self.query_date_to())

            context = {
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
            messages.error(
                request, 'Falta una configuraci??n, le recomedamos comunicarse con el administrador del sistema')
            return redirect('orders:index')

        if not time_in_range(setting.time_limit_to, setting.time_limit_from, get_time_now()):
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
        'title': 'Pedido - Direcciones de env??o'
    })


@login_required()
@permission_required('orders.add_order', raise_exception=True)
def payment_view(request):
    template_name = 'orders/payment.html'
    order = get_or_create_order(request)
    if request.method == 'POST':
        if 'payed_image' in request.FILES and order.total > 0:
            if order.detail_set.count() == 0:
                messages.error(
                    request, 'El pedido no tiene ninguna direcci??n de env??o')
            order.payed_order(
                payed_image=request.FILES['payed_image'],
                type_ticket=request.POST.get('type_ticket'),
                business_name=request.POST.get('business_name'),
                ruc=request.POST.get('ruc'),
            )
            for detail in order.detail_set.all():
                if detail.tracking_code is None:
                    detail.payed(
                        tracking_code=get_generate_tracking_code(),
                    )
                if detail.tracking_code:
                    if detail.address_origin.email:
                        thread = threading.Thread(
                            target=Mail.send_complete_order,
                            args=(detail, detail.address_origin.full_name,
                                  detail.address_origin.email, request)
                        )
                        thread.start()
                    if detail.address_destiny.email:
                        thread2 = threading.Thread(
                            target=Mail.send_complete_order,
                            args=(detail, detail.address_destiny.full_name,
                                  detail.address_destiny.email, request)
                        )
                        thread2.start()
                    TrackingOrder.objects.create(
                        detail=detail,
                        location='Pendiente a recojer en el direcci??n ingresada.'
                    )
                    if not detail.is_unassign_delivery:
                        UnassignDeliveryAddress.objects.create(detail=detail)
                    if not detail.is_unassign_origin:
                        UnassignOriginAddress.objects.create(detail=detail)
            return redirect('orders:payment-success')
        else:
            messages.error(
                request, 'Usted no ha realizado el pago, siga la forma de pago')

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

            context = {
                'filename': 'rotulado-{}'.format(order.pk),
                'date': datetime.now().date(),
                'logo': 'img/logo.png',
                'ui': 'img/report/ui-rotulado.png',
                'order': order,
            }
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(
                context['filename'])
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
                UnassignOriginAddress.objects.filter(
                    detail=detail).first().delete()
        messages.success(
            request, 'Direccion(es) de recojo asignada(s) con ??xito')
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
                UnassignDeliveryAddress.objects.filter(
                    detail=detail).first().delete()
        messages.success(
            request, 'Direccion(es) de entrega asignada(s) con ??xito')
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
            messages.success(
                request, 'La direcci??n de recojo, dej?? de ser asignada al motorizado.')
            return redirect("orders:origins")
        messages.success(
            request, 'La direcci??n de recojo, ya dej?? de ser asignada previamente.')
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
            AssignDeliveryAddress.objects.filter(
                detail=detail).first().delete()
            messages.success(
                request, 'La direcci??n de env??o, dej?? de ser asignada al motorizado.')
            return redirect("orders:deliveries")
        messages.success(
            request, 'La direcci??n de env??o, ya dej?? de ser asignada previamente.')
        return redirect("orders:deliveries")


class ReportOrdersPDFView(View):
    def query(self):
        return self.request.GET.get('q')

    def query_date_from(self):
        return self.request.GET.get('date_from')

    def query_date_to(self):
        return self.request.GET.get('date_to')

    def query_status(self):
        return self.request.GET.get('status')

    def query_origin(self):
        return self.request.GET.get('origin')

    def query_destiny(self):
        return self.request.GET.get('destiny')

    def query_type_ticket(self):
        return self.request.GET.get('type_ticket')

    def get(self, request, *args, **kwargs):
        try:
            template_name = 'orders/report/order-list.html'
            orders = Detail.objects.exclude(tracking_code=None).search_detail_and_client(self.query()).search_by_address_origin(self.query_origin()).search_by_address_delivery(
                self.query_destiny()).search_by_status(self.query_status()).search_date_from(self.query_date_from()).search_date_to(self.query_date_to()).search_type_ticket(self.query_type_ticket())
            date_now = datetime.now().strftime("%d-%m-%Y")

            context = {
                'filename': 'reporte-ordenes-pdf-{}'.format(date_now),
                'date': date_now,
                'logo': 'img/logo.png',
                'ui': 'img/report/ui-rotulado.png',
                'orders': orders,
            }
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(
                context['filename'])
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
        date_now = datetime.now().strftime("%d-%m-%Y")
        filename = 'reporte-ordenes-excel-{}'.format(date_now),
        headers = ['# Tracking', 'Cliente', 'Fecha', 'Direcci??n',
                   'Quien atender??', 'Celular', 'Precio S/']
        name_sheet = 'Ordenes'

        qs = Detail.objects.search_detail_and_client(self.query()).search_by_address_origin(self.query_origin(
        )).search_by_address_delivery(self.query_destiny()).search_by_status(self.query_status()).search_by_date(self.query_date())
        dict_qs = [{'tracking_code': detail.tracking_code,
                    'client': detail.client.full_name(),
                    'created_at': detail.get_created_at_format(),
                    'address_destiny': detail.address_destiny.address_complete(),
                    'address_client': detail.address_destiny.full_name,
                    'address_cell_phone': detail.address_destiny.cell_phone,
                    'price_rate': detail.price_rate
                    } for detail in qs]
        df = pd.DataFrame(dict_qs)
        with BytesIO() as b:
            # Use the StringIO object as the filehandle.
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            df.to_excel(writer, sheet_name=name_sheet, index=False)
            # Get the xlsxwriter workbook and worksheet objects.
            workbook = writer.book
            worksheet = writer.sheets[name_sheet]

            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1})
            for col_num, value in enumerate(headers):
                worksheet.write(0, col_num, value, header_format)
            writer.save()
            # Set up the Http response.
            response = HttpResponse(
                b.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % filename
            return response


def export_orders_excel_view(request):
    query = request.GET.get('q')
    query_status = request.GET.get('status')
    query_origin = request.GET.get('origin')
    query_destiny = request.GET.get('destiny')
    query_date_from = request.GET.get('date_from')
    query_date_to = request.GET.get('date_to')
    query_type_ticket = request.GET.get('type_ticket')

    date_now = datetime.now().strftime("%d-%m-%Y")
    filename = 'reporte-ordenes-excel-{}'.format(date_now),
    headers = ['# Tracking', 'Cliente', 'Fecha', 'Direcci??n',
               'Quien atender??', 'Celular', 'Precio S/']
    name_sheet = 'Ordenes'

    qs = Detail.objects.exclude(tracking_code=None).search_detail_and_client(query).search_by_address_origin(query_origin).search_by_address_delivery(
        query_destiny).search_by_status(query_status).search_date_from(query_date_from).search_date_to(query_date_to).search_type_ticket(query_type_ticket)
    dict_qs = [{'tracking_code': detail.tracking_code,
                'client': detail.client.full_name(),
                'created_at': detail.get_created_at_format(),
                'address_destiny': detail.address_destiny.address_complete(),
                'address_client': detail.address_destiny.full_name,
                'address_cell_phone': detail.address_destiny.cell_phone,
                'price_rate': detail.price_rate
                } for detail in qs]
    df = pd.DataFrame(dict_qs)
    with BytesIO() as b:

        writer = pd.ExcelWriter(b, engine='xlsxwriter')
        df.to_excel(writer, sheet_name=name_sheet, index=False)
        workbook = writer.book

        worksheet = writer.sheets[name_sheet]

        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1})

        for col_num, value in enumerate(headers):
            worksheet.write(0, col_num, value, header_format)

        writer.save()

        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s.xlsx' % filename

        return response
