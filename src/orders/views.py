from django.contrib import messages
from wsgiref.util import request_uri
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

# Create your views here.
from carts.utils import get_or_create_cart
from carts.utils import destroy_cart
from orders.models import Order
from orders.utils import breadcrumb
from orders.utils import get_or_create_order
from orders.utils import destroy_order
from shipping_address.models import ShippingAddress
from orders.mails import Mail

def get_cart_order(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)
    return cart, order

@login_required(login_url='login')
def order(request):
    cart, order = get_cart_order(request)
    return render(request, 'order.html', {
        'cart':cart, 
        'order':order,
        'breadcrumb': breadcrumb(products=True),
    })

@login_required(login_url='login')
def address(request):
    cart, order = get_cart_order(request)

    shipping_address = order.get_or_set_shipping_address()
    can_choose_address = request.user.shippingaddress_set.count() > 1
    return render(request, 'address.html', {
        'cart' :cart,
        'order': order,
        'shipping_address': shipping_address,
        'breadcrumb' : breadcrumb(products=True, address=True),
        'can_choose_address' : can_choose_address,
    })


@login_required(login_url='login')
def select_address(request):
    shipping_address = request.user.shippingaddress_set.all()
    return render(request, 'select_address.html', {
        'breadcrumb' : breadcrumb(products=True, address=True),
        'shipping_address' : shipping_address,
    })

@login_required(login_url='login')
def check_address(request, pk):
    cart, order = get_cart_order(request)
    shipping_address = get_object_or_404(ShippingAddress, pk = pk)

    if request.user.id != shipping_address.user.id:
        return redirect('carts:cart')

    order.update_shipping_address(shipping_address)
    return redirect('orders:address')

@login_required(login_url='login')
def confirm(request):
    cart, order = get_cart_order(request)
    shipping_address = order.shipping_address

    if shipping_address is None:
        return redirect('orders:address')
    
    return render(request, 'confirm.html', {
        'cart': cart,
        'order': order,
        'shipping_address': shipping_address,
        'breadcrumb': breadcrumb(products=True, address=True, confirmation=True),
    })

@login_required(login_url='login')
def cancel(request):
    cart, order = get_cart_order(request)
    #cart = get_or_create_cart(request)
    #order = get_or_create_order(cart, request)

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.cancel()
    destroy_order(request)
    destroy_cart(request)

    messages.error(request, 'Orden cancelada')
    return redirect('main')

@login_required(login_url='login')
def complete(request):
    cart, order = get_cart_order(request)

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    Mail.send_complete_order(order, request.user)

    order.complete()
    destroy_order(request)
    destroy_cart(request)

    messages.success(request, 'Orden creada exitosamente :D')
    return redirect('main')
