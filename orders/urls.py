from django.urls import path 

from .views import OrderListView, add_addresses_view, cancel_order_view, create_order_client_view, create_order_view
from details.views import create_detail_view, update_client_view

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='index'),
    path('create-client/', create_order_client_view, name="create-client"),
    path('create/', create_order_view, name="create"),
    path('create/detail/create/', create_detail_view, name="create-detail"),
    path('create-client/detail/<int:pk>/update/', update_client_view, name="update-detail"),
    path('cancel-order/', cancel_order_view, name="cancel-order"),
    path('add-addresses/', add_addresses_view, name="add-addresses"),
]