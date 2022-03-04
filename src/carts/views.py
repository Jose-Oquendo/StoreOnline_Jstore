from asyncio import ProactorEventLoop
from itertools import product
from math import prod
from django.shortcuts import render
from carts.models import Cart
# Create your views here.

from carts.utils import get_or_create_cart
from carts.models import Cart
from products.models import Product

def cart(request):
    cart = get_or_create_cart(request)
    return render(request, 'carts/carts.html', {'cart':cart}) #ojo


def add(request):
    cart = get_or_create_cart(request)
    print('Hola este es el error ', request.POST.get('product_id'))
    num_id = request.POST.get('product_id')
    product2 = Product.objects.get(pk=num_id)
    cart.products.add(product2)
    print('este es el producto ', product2)

    return render(request, 'carts/add.html', {
        'product': product2
    })