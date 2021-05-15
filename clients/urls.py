from django.urls import path

from .views import ClientDeleteView, ClientDetailView, ClientListVew, ClientUpdateView, client_create_view, complete_address_client_update_view, complete_address_client_view, get_clients_view

app_name = 'clients'

urlpatterns = [
    path('', ClientListVew.as_view(), name="index"),
    path('<int:pk>/create/', client_create_view, name="create"),
    path('<slug:slug>/complete-address/', complete_address_client_view, name="complete-address"),
    path('<slug:slug>/complete-address-update/', complete_address_client_update_view, name="complete-address-update"),
    path('get-clients/', get_clients_view),
    path('<slug:slug>/', ClientDetailView.as_view(), name="detail"),
    path('<slug:slug>/update/', ClientUpdateView.as_view(), name="update"),
    path('<slug:slug>/delete/', ClientDeleteView.as_view(), name="delete"),
]