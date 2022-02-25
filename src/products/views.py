from unicodedata import category
from django.shortcuts import render
from products.models import Product
from django.views import generic
from django.db.models import Q
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

class ProductSearchView(generic.ListView):
    template_name = 'search.html'

    def get_queryset(self):
        filter = Q(tittle__icontains = self.query() | Q(category_tittle_icontains = self.query()))
        return Product.objects.filter(filter)

    def query(self):
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['count'] = context['product_list'].count()
        return context
