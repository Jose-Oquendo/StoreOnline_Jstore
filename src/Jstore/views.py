from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context={
        'title' : 'index',
        'message' : 'Nuevo mensaje desde la vista',
        'products' : [
            {'title':'Playera', 'price':20000, 'stock':True},
            {'title':'Blusa', 'price':16000, 'stock':True},
            {'title':'Mochila', 'price':30000, 'stock':True},
        ]
    }
    return render(request, 'index.html', context)
