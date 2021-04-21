from django.urls import path

from .views import get_service_prices

app_name = 'service_prices'

urlpatterns = [
    path('get-service-prices/', get_service_prices)
]