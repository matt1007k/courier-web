from django.urls import path 

from .views import create_order_client_view
from details.views import create_client_view, update_client_view

app_name = 'orders'

urlpatterns = [
    path('create-client/', create_order_client_view, name="create-client"),
    path('create-client/detail/create/', create_client_view, name="create-detail"),
    path('create-client/detail/<int:pk>/update/', update_client_view, name="update-detail"),
]