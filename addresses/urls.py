from django.urls import path

from .views import AddressCreateView, AddressListView, AddressUpdateView, AddressDeleteView, default_view

app_name = 'addresses'

urlpatterns = [
    path('', AddressListView.as_view(), name="index"),
    path('create/', AddressCreateView.as_view(), name="create"),
    path('<int:pk>/update/', AddressUpdateView.as_view(), name="update"),
    path('<int:pk>/delete/', AddressDeleteView.as_view(), name="delete"),
    path('<int:pk>/default/', default_view, name="default"),
]