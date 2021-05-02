from django.urls import path

from .views import ClientDeleteView, ClientDetailView, ClientListVew, ClientUpdateView, ClienteCreateView, get_clients_view

app_name = 'clients'

urlpatterns = [
    path('', ClientListVew.as_view(), name="index"),
    path('create/', ClienteCreateView.as_view(), name="create"),
    path('get-clients/', get_clients_view),
    path('<slug:slug>/', ClientDetailView.as_view(), name="detail"),
    path('<slug:slug>/update/', ClientUpdateView.as_view(), name="update"),
    path('<slug:slug>/delete/', ClientDeleteView.as_view(), name="delete"),
]