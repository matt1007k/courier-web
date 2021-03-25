from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from .utils import get_or_create_order
from .models import Order

@login_required()
def create_order_client_view(request):
    order = get_or_create_order(request) 
        
    return render(request, 'orders/create-client.html', context={
        'order': order
    })