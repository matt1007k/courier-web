from django.contrib import messages
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required

from .utils import get_or_create_order
from .models import Order

@login_required()
def create_order_client_view(request):
    order = get_or_create_order(request) 
    if request.method == 'POST':
        if 'image_payed' in request.FILES:
            if order.detail_set.count() == 0:
                messages.error(request, 'El pedido no tiene ningún elemento de envió')
            image_payed = request.FILES['image_payed']
            order.image_payed = image_payed
            order.save()
            messages.success(request, 'El pedido se ha realizado con exitó')
            # return redirect('orders:index') 
        else:
            messages.error(request, 'Usted no ha realizado el pago, siga la forma de pago')
        
    return render(request, 'orders/create-client.html', context={
        'order': order
    })