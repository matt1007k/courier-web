import json
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

    # if promo_code.discount > 0:
    #     order.apply_promo_code(promo_code)
    #     total_previous = order.get_total_previous()
    #     discount = order.get_discount()
        
    # if promo_code.special > 0:
    #     order.apply_promo_code_special(promo_code)
    #     total_previous = order.get_total_previous_special()
    #     discount = order.get_discount_special()

    return JsonResponse({
        'status': True,
        'is_discount': promo_code.discount > 0,
        'is_special': promo_code.special > 0,
        'order_id': order.pk
    }, status=200)

    # return JsonResponse(data={
    #     'status': True,
    #     'code': promo_code.code,
    #     'discount': discount,
    #     'total_previous': total_previous,
    #     'sub_total': order.get_sub_total(),
    #     'igv': order.get_igv(),
    #     'price_rate_previous_list': order.get_price_rate_previous_list(),
    #     'price_rate_list': order.get_price_rate_list(),
    #     'total': order.get_format_total()
    # }, status=200)