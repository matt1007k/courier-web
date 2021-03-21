from django.urls import path

from .views import DriverCreateView, DriverDetailView, DriverListView, DriverUpdateView, DriverDeleteView, VehicleCreateView, VehicleUpdateView

app_name='drivers'

urlpatterns = [
    path('', DriverListView.as_view(), name='index'),
    path('create/', DriverCreateView.as_view(), name='create'),
    path('vehicle-create/', VehicleCreateView.as_view(), name='create-vehicle'),
    path('<pk>/vehicle-create/', VehicleUpdateView.as_view(), name='update-vehicle'),
    path('<slug:slug>/', DriverDetailView.as_view(), name='detail'),
    path('<slug:slug>/update/', DriverUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', DriverDeleteView.as_view(), name='delete'),
]