from turtle import title
from django.http import JsonResponse
from django.shortcuts import render
from orders.decorator import validate_cart_and_order

# Create your views here.
from promo_code.models import PromoCode

@validate_cart_and_order
def validate(request, cart, order):
    code = request.GET.get('code')
    promo_code = PromoCode.objects.filter(code=code).first()
    if promo_code is None:
        return JsonResponse({
            'status':False
        }, status= 404)

    order.apply_promo_code(promo_code)
        
    return JsonResponse({
        'status' : True,
        'code': promo_code.code,
        'discount' : promo_code.discount,
        'total' : order.total,
    })