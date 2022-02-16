from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context={
        'title' : 'index',
        'message' : 'Nuevo mensaje desde la vista',
        'products' : [
            {'title':'Playera', 'price':20000, 'stock':True, 'img': "static/img/playera.jpg"},
            {'title':'Blusa', 'price':16000, 'stock':True, 'img': "static/img/blusa.jpg"},
            {'title':'Mochila', 'price':30000, 'stock':True, 'img': "static/img/bolso.jpg"},
        ]
    }
    return render(request, 'index.html', context)

def login(request):
    return render(request, 'user/login.html')