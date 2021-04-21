"""courier_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from .views import dashboard

handler404 = 'pages.views.error_404' #DEBUG = False production

urlpatterns = [
    path('', include('pages.urls', namespace="index")),
    path('dashboard/', dashboard, name="dash"),
    path('auth/', include('authentication.urls', namespace='auth')),
    path('addresses/', include('addresses.urls', namespace='addresses')),
    path('clients/', include('clients.urls', namespace='clients')),
    path('drivers/', include('drivers.urls', namespace='drivers')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('details/', include('details.urls', namespace='details')),
    path('promo-codes/', include('promo_codes.urls', namespace='promo_codes')),
    path('service-prices/', include('service_prices.urls', namespace='service_prices')),
    path('admin/', admin.site.urls),
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)