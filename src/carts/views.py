from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from carts.models import Cart
from carts.models import CartProduct
from carts.models import CartProductManager
from carts.utils import get_or_create_cart
from products.models import Product

def cart(request):
    cart = get_or_create_cart(request)
    cart2 = cart.products.all()
    return render(request, 'carts/carts.html', {'cart':cart})

def add(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    #product = Product.objects.get(pk=request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity', 1))
    cart_product = CartProduct.objects.create_or_update_quantity(cart = cart,
        product = product,
        quantity =  quantity,
    )
   
    return render(request, 'carts/add.html', {
        'quantity' : quantity,
        'cart_product' : cart_product,
        'product': product,
    })

def remove(request):
    cart = get_or_create_cart(request)
    product = Product.objects.get(pk=request.POST.get('product_id'))

    cart.products.remove(product)
    return redirect('carts:carts')