from django.urls import path

from .views import AddressCreateView, AddressListView, AddressUpdateView, AddressDeleteView, default_view, get_address_client_view

app_name = 'addresses'

urlpatterns = [
    path('', AddressListView.as_view(), name="index"),
    path('get-address/<slug:slug>/', get_address_client_view),
    path('create/', AddressCreateView.as_view(), name="create"),
    path('<int:pk>/update/', AddressUpdateView.as_view(), name="update"),
    path('<int:pk>/delete/', AddressDeleteView.as_view(), name="delete"),
    path('<int:pk>/default/', default_view, name="default"),

]