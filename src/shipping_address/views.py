from django.shortcuts import render
from numpy import generic

# Create your views here.
from shipping_address.models import ShippingAddress

class ShippingAddressListView(generic.ListView):
    model = ShippingAddress
    template_name = 'shipping_addresses.html'

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')
