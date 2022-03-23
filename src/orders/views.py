import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from carts.utils import get_or_create_cart
from orders.models import Order
from orders.utils import breadcrumb, get_or_create_order

@login_required(login_url='login')
def order(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)
    return render(request, 'order.html', {
        'cart':cart, 
        'order':order,
        'breadcrumb': breadcrumb(products=True),
    })

@login_required(login_url='login')
def address(request):

    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    shipping_address = order.get_or_set_shipping_address()
    return render(request, 'address.html', {
        'cart' :cart,
        'order': order,
        'shipping_address': shipping_address,
        'breadcrumb' : breadcrumb(products=True, address=True),
    })


@login_required(login_url='login')
def select_address(request):
    shipping_address = request.user.shippingaddress_set.all()
    return render(request, 'select_address.html', {
        'breadcrumb' : breadcrumb(products=True, address=True),
        'shipping_address' : shipping_address,
    })