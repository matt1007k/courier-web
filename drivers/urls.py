from django.urls import path

from .views import DriverCreateView, DriverDetailView, DriverListView, DriverUpdateView, DriverDeleteView, VehicleCreateView, VehicleUpdateView, get_driver_view, payment_account_create_view, payment_account_update_view
from valorations.views import create_valoration_view

app_name='drivers'

urlpatterns = [
    path('', DriverListView.as_view(), name='index'),
    path('get-drivers/', get_driver_view),
    path('create/', DriverCreateView.as_view(), name='create'),
    path('vehicle-create/', VehicleCreateView.as_view(), name='create-vehicle'),
    path('<pk>/vehicle-create/', VehicleUpdateView.as_view(), name='update-vehicle'),
    path('<slug:slug>/', DriverDetailView.as_view(), name='detail'),
    path('<slug:slug>/update/', DriverUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', DriverDeleteView.as_view(), name='delete'),
    path('<slug:slug>/valoration/', create_valoration_view, name='valoration'),
    path('<slug:slug>/payment-account/create', payment_account_create_view, name='payment-account'),
    path('<slug:slug>/payment-account/edit', payment_account_update_view, name='payment-account.update'),
]