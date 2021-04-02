from django.urls import path 

from .views import OrderListView, create_order_client_view, create_order_view
from details.views import create_client_view, update_client_view

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='index'),
    path('create-client/', create_order_client_view, name="create-client"),
    path('create/', create_order_view, name="create"),
    path('create-client/detail/create/', create_client_view, name="create-detail"),
    path('create-client/detail/<int:pk>/update/', update_client_view, name="update-detail"),
]