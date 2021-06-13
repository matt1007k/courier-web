from django.urls import path

from .views import DeleteDetailView, PackageDetailView, change_status_view, not_on_routed_delivery_view, not_on_routed_origin_view, origin_map_view, destiny_map_view, package_delivered_view, package_tracking_view, received_package_view
from .api import DetailApiListView, StatusDetailApiViewList

app_name = 'details'

urlpatterns = [
    path('<int:pk>/paquete/', PackageDetailView.as_view(), name="detail"),
    path('<int:pk>/status/change', change_status_view, name="change-status"),
    path('<int:pk>/delete/', DeleteDetailView.as_view(), name="delete"),
    path('<int:pk>/origin-map/', origin_map_view, name="origin-map"),
    path('<int:pk>/destiny-map/', destiny_map_view, name="destiny-map"),
    path('<int:pk>/received/', received_package_view, name="received"),
    path('<int:pk>/not-onrouted-origin/', not_on_routed_origin_view, name="not-onrouted-origin"),
    path('<str:tracking_code>/tracking/', package_tracking_view, name="tracking"),
    path('<int:pk>/not-onrouted-delivery/', not_on_routed_delivery_view, name="not-onrouted-delivery"),
    path('<int:pk>/package-delivered/', package_delivered_view, name="package-delivered"),
    path('api/', DetailApiListView.as_view(), name="list-api"),
    path('api/statuses/', StatusDetailApiViewList.as_view(), name="list-api-statuses"),
]