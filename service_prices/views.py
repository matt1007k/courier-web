from django.shortcuts import render
from django.core.serializers import serialize
from django.http.response import JsonResponse 
from django.http import HttpResponse

from .models import ServicePrice

def get_service_prices(request):
    service_prices = ServicePrice.objects.all()
    data = serialize('json', service_prices)
    
    return HttpResponse(data, content_type='application/json', status=200)