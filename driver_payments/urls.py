from driver_payments.views import DriverPaymentListView
from django.urls import path

app_name = 'driver_payments'

urlpatterns = [
    path('', DriverPaymentListView.as_view(), name='index'),
]