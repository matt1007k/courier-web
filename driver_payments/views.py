from typing import Any, Dict
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import DriverPayment

class DriverPaymentListView(LoginRequiredMixin, ListView):
    template_name = 'driver_payments/index.html'
    model = DriverPayment

    def query_driver(self):
        return self.request.GET.get('driver')

    def query_date_to(self):
        return self.request.GET.get('date_to')

    def query_date_from(self):
        return self.request.GET.get('date_from')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Mis pagos' if self.request.user.is_driver else 'Pagos del motorizado'
        return context

    def get_queryset(self):
        if self.request.user.is_driver:
            object_list = self.request.user.driver.driverpayment_set.all().order_by('-id')
        else:
            object_list = self.model.objects.all().order_by('-id')

        object_list = object_list.search_driver(self.query_driver()).search_date_from(self.query_date_from()).search_date_to(self.query_date_to())
        return object_list
