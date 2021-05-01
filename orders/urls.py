from django.urls import path 

from .views import DetailOrderView, OrderDeliveryListView, OrderListView, OrderOriginListView, add_addresses_view, assign_order_view, cancel_order_view, create_order_client_view, create_order_view, payment_success_view, payment_view, tracking_order_view
from details.views import create_detail_view, update_detail_view

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='index'),
    path('origins/', OrderOriginListView.as_view(), name='origins'),
    path('deliveries/', OrderDeliveryListView.as_view(), name='deliveries'),
    path('create-client/', create_order_client_view, name="create-client"),
    path('create/', create_order_view, name="create"),
    path('create/detail/create/', create_detail_view, name="create-detail"),
    path('create/detail/<int:pk>/update/', update_detail_view, name="update-detail"),
    path('cancel-order/', cancel_order_view, name="cancel-order"),
    path('add-addresses/', add_addresses_view, name="add-addresses"),
    path('payment/', payment_view, name="payment"),
    path('payment-success/', payment_success_view, name="payment-success"),
    path('tracking-order/', tracking_order_view),
    path('<int:pk>/', DetailOrderView.as_view(), name='detail'),
    path('<int:pk>/assign/', assign_order_view, name='assign'),
]