from sre_constants import SUCCESS
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

from products.models import Product
from Jstore.forms import RegisterForm

def index(request):
    products = Product.objects.all().order_by('tittle')
    context={
        'title' : 'Products',
        'message' : 'Productos de nuestra tienda',
        'products' : products,
    }
    return render(request, 'index.html', context)


#-------------------------main-----------------------------------------------
def main(request):
    return render(request, 'users/main.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('products/index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            return redirect('products/index') #se redirecciona al name en las urls
        else:
            messages.error(request, 'Usuario o contraseña No validos')
    return render(request, 'users/login.html')

def logout_view(request):    
    logout(request)
    messages.success(request, 'Sesion cerrada correctamente' )
    return redirect('login')

def register(request):
    form = RegisterForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect('products/index')
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if user:
            login(request, user)
            messages.success(request, 'Usuario creado de forma exitosa')
            return redirect('products/index')
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)
