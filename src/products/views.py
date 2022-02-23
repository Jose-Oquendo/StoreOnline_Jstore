from pyexpat import model
from django.shortcuts import render
from products.models import Product
from django.views import generic
# Create your views here.

from products.models import Product

class ProductListView(generic.ListView):
    template_name = 'index.html'
    queryset = Product.objects.all().order_by('tittle')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Listado de productos'
        context['products'] = context['object_list']
        return context

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product.html'
