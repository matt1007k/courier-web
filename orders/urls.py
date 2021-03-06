from django.urls import path 

from .views import ( 
    AssignDeliveryAddressListView, 
    DetailOrderView, 
    ExportOrdersExcelView, 
    AssignOriginAddressListView, 
    ReportOrdersPDFView, 
    ReportRotuladoView, 
    ReporteAssignDeliveryAddressView, 
    ReporteAssignOriginAddressView, 
    UnassignDeliveryAddressListView, 
    UnassignOriginAddressListAPIView, 
    UnassignOriginAddressListView, 
    add_addresses_view, 
    assign_deliveries_to_driver_view, 
    assign_origins_to_driver_view, 
    cancel_order_view, 
    create_order_view,
    export_orders_excel_view, 
    get_client_view,
    index, 
    payment_success_view, 
    payment_view, 
    return_unassign_delivery_view, 
    tracking_order_view, 
    return_unassign_origin_view
)
from details.views import create_detail_view, update_detail_view

app_name = 'orders'

urlpatterns = [
    path('', index, name='index'),
    path('get-client/', get_client_view),
    path('origins/', AssignOriginAddressListView.as_view(), name='origins'),
    path('origins/report/', ReporteAssignOriginAddressView.as_view(), name='origins-report'),
    path('deliveries/', AssignDeliveryAddressListView.as_view(), name='deliveries'),
    path('deliveries/report/', ReporteAssignDeliveryAddressView.as_view(), name='deliveries-report'),
    path('unassign-origins/', UnassignOriginAddressListView.as_view(), name='unassign-origins'),
    path('assign-origins/', assign_origins_to_driver_view, name='assign-origins'),
    path('<int:pk>/return-unassign-origin/', return_unassign_origin_view, name="return-unassign-origin"),
    path('assign-deliveries/', assign_deliveries_to_driver_view, name='assign-deliveries'),
    path('get-unassign-origins/', UnassignOriginAddressListAPIView.as_view()),
    path('unassign-deliveries/', UnassignDeliveryAddressListView.as_view(), name='unassign-deliveries'),
    path('<int:pk>/return-unassign-delivery/', return_unassign_delivery_view, name="return-unassign-delivery"),
    path('create/', create_order_view, name="create"),
    path('create/detail/create/', create_detail_view, name="create-detail"),
    path('create/detail/<int:pk>/update/', update_detail_view, name="update-detail"),
    path('cancel-order/', cancel_order_view, name="cancel-order"),
    path('add-addresses/', add_addresses_view, name="add-addresses"),
    path('payment/', payment_view, name="payment"),
    path('payment-success/', payment_success_view, name="payment-success"),
    path('tracking-order/', tracking_order_view),
    path('exportPDF/', ReportOrdersPDFView.as_view(), name="export-pdf"),
    path('exportExcel/', export_orders_excel_view, name="export-excel"),
    path('<int:pk>/', DetailOrderView.as_view(), name='detail'),
    path('<int:pk>/rotulado/', ReportRotuladoView.as_view(), name='rotulado'),
]