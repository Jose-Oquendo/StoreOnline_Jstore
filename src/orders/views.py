import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from carts.utils import get_or_create_cart
from orders.models import Order
from orders.utils import breadcrumb, get_or_create_order
import shipping_address

@login_required(login_url='login')
def order(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)
    return render(request, 'order.html', {
        'cart':cart, 
        'order':order,
        'breadcrumb': breadcrumb(request),
    })

@login_required(login_url='login')
def address(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    shipping_address = order.shipping_address
    return render(request, 'address.html', {
        'cart' :cart,
        'order': order,
        'breadcrumb' : breadcrumb(address=True),
    })