from concurrent.futures import thread
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models.query import EmptyQuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View, generic
import threading

# Create your views here.
from carts.utils import get_or_create_cart
from carts.utils import destroy_cart
from orders.decorator import validate_cart_and_order
from orders.models import Order
from orders.mails import Mail
from orders.utils import breadcrumb
from orders.utils import get_or_create_order
from orders.utils import destroy_order
from shipping_address.models import ShippingAddress

@login_required(login_url='login')
@validate_cart_and_order
def order(request, cart, order):
    return render(request, 'order.html', {
        'cart':cart, 
        'order':order,
        'breadcrumb': breadcrumb(products=True),
    })

@login_required(login_url='login')
@validate_cart_and_order
def address(request, cart, order):
    shipping_address = order.get_or_set_shipping_address()
    can_choose_address = request.user.has_shipping_addresses
    return render(request, 'address.html', {
        'cart' :cart,
        'order': order,
        'shipping_address': shipping_address,
        'breadcrumb' : breadcrumb(products=True, address=True),
        'can_choose_address' : can_choose_address,
    })

@login_required(login_url='login')
def select_address(request):
    shipping_address = request.user.addresses
    return render(request, 'select_address.html', {
        'breadcrumb' : breadcrumb(products=True, address=True),
        'shipping_address' : shipping_address,
    })

@login_required(login_url='login')
@validate_cart_and_order
def check_address(request, cart, order, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk = pk)

    if request.user.id != shipping_address.user.id:
        return redirect('carts:cart')

    order.update_shipping_address(shipping_address)
    return redirect('orders:address')

@login_required(login_url='login')
@validate_cart_and_order
def confirm(request, cart, order):
    shipping_address = order.shipping_address

    if shipping_address is None:
        return redirect('orders:address')
    
    return render(request, 'confirm.html', {
        'cart': cart,
        'order': order,
        'shipping_address': shipping_address,
        'breadcrumb': breadcrumb(products=True, address=True, payment=True, confirmation=True),
    })

@login_required(login_url='login')
@validate_cart_and_order
def to_pay(request, cart, order):
    return render(request, 'payment.html', {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb(products=True, address=True, payment=True),
    })

@login_required(login_url='login')
@validate_cart_and_order
def cancel(request, cart, order):
    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.cancel()
    destroy_order(request)
    destroy_cart(request)

    messages.error(request, 'Orden cancelada')
    return redirect('main')

@login_required(login_url='login')
@validate_cart_and_order
def complete(request , cart, order):
    if request.user.id != order.user_id:
        return redirect('carts:cart')

    thread = threading.Thread(target=Mail.send_complete_order, args=(
        order, request.user
    ))

    Mail.send_complete_order(order, request.user)

    order.complete()
    destroy_order(request)
    destroy_cart(request)

    messages.success(request, 'Orden creada exitosamente :D')
    return redirect('main')

class OrderListView(LoginRequiredMixin, generic.ListView):
    login_url = 'login'
    template_name = 'orders.html'

    def get_queryset(self):
        return self.request.user.orders_completed()

