from django import conf
from django.urls import reverse
from orders.models import Order

def get_or_create_order(cart, request):
    order = cart.order

    if order is None and request.user.is_authenticated:
        order = Order.objects.create(cart=cart, 
            user=request.user,
        )
    if order:
        request.session['order_id'] = order.id
    return order

def breadcrumb(products = False, address=False, payment=False, confirmation=False):
    return (
        {'title':'Productos', 'activate': products, 'url':reverse('orders:order')},
        {'title':'Dirección', 'activate': address, 'url':reverse('orders:address')},#('orders:address')
        {'title':'Pago', 'activate': payment, 'url':reverse('orders:order')},
        {'title':'Confirmacón', 'activate': confirmation, 'url':reverse('orders:confirm')},
    )

def destroy_order(request):
    request.session['order_id'] = None