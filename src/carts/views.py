from asyncio import ProactorEventLoop
from itertools import product
from math import prod
from this import d
from webbrowser import get
from django.shortcuts import render, redirect, get_object_or_404
from carts.models import Cart
# Create your views here.

from carts.utils import get_or_create_cart
from carts.models import Cart
from products.models import Product

def cart(request):
    cart = get_or_create_cart(request)
    cart2 = cart.products.all()
    return render(request, 'carts/carts.html', {'cart':cart}) #ojo


def add(request):
    cart = get_or_create_cart(request)
    product2 = Product.objects.get(pk=request.POST.get('product_id'))
    prod = get_object_or_404(Product, pk=request.POST.get('product_id'))
    cart.products.add(product2)
    return render(request, 'carts/add.html', {
        'product': product2
    })

def remove(request):
    cart = get_or_create_cart(request)
    product = Product.objects.get(pk=request.POST.get('product_id'))
    prod = get_object_or_404(Product, pk=request.POST.get('product_id'))
    cart.products.remove(product)
    return redirect('carts:carts')