from django.urls import path 

from .views import AssignDeliveryAddressListView, DetailOrderView, OrderListView, AssignOriginAddressListView, UnassignDeliveryAddressListView, UnassignOriginAddressListAPIView, UnassignOriginAddressListView, add_addresses_view, assign_deliveries_to_driver_view, assign_origins_to_driver_view, cancel_order_view, create_order_view, get_client_view, payment_success_view, payment_view, tracking_order_view 
from details.views import create_detail_view, update_detail_view

app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='index'),
    path('get-client/', get_client_view),
    path('origins/', AssignOriginAddressListView.as_view(), name='origins'),
    path('deliveries/', AssignDeliveryAddressListView.as_view(), name='deliveries'),
    path('unassign-origins/', UnassignOriginAddressListView.as_view(), name='unassign-origins'),
    path('assign-origins/', assign_origins_to_driver_view, name='assign-origins'),
    path('assign-deliveries/', assign_deliveries_to_driver_view, name='assign-deliveries'),
    path('get-unassign-origins/', UnassignOriginAddressListAPIView.as_view()),
    path('unassign-deliveries/', UnassignDeliveryAddressListView.as_view(), name='unassign-deliveries'),
    path('create/', create_order_view, name="create"),
    path('create/detail/create/', create_detail_view, name="create-detail"),
    path('create/detail/<int:pk>/update/', update_detail_view, name="update-detail"),
    path('cancel-order/', cancel_order_view, name="cancel-order"),
    path('add-addresses/', add_addresses_view, name="add-addresses"),
    path('payment/', payment_view, name="payment"),
    path('payment-success/', payment_success_view, name="payment-success"),
    path('tracking-order/', tracking_order_view),
    path('<int:pk>/', DetailOrderView.as_view(), name='detail'),
]