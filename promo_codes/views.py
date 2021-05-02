import decimal
from django.http.response import JsonResponse
from django.shortcuts import render
from .models import PromoCode

from orders.utils import get_or_create_order

def validate_code_view(request):
    order = get_or_create_order(request)

    code = request.GET.get('code')
    promo_code = PromoCode.objects.get_valid(code)

    if promo_code is None:
        return JsonResponse({
            'status': False
        }, status=404)

    order.apply_promo_code(promo_code)

    return JsonResponse(data={
        'status': True,
        'code': promo_code.code,
        'discount': order.get_discount(),
        'total_previous': order.get_total_previous(),
        'sub_total': round(float(order.sub_total), 2),
        'igv': round(float(order.igv), 2),
        'total': order.total
    }, status=200)