from re import template
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from shipping_address.forms import ShippingForm
from shipping_address.models import ShippingAddress

@login_required(login_url='login')
def create(request):
    form = ShippingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        shipping_address = form.save(commit=False)
        shipping_address.user = request.user
        shipping_address.default = not ShippingAddress.objects.filter(user=request.user).exists()
        shipping_address.save()
        messages.success(request,'Direccion creada con exito')
        return redirect('shipping_address:shipping_address')
    return render(request, 'create.html', {'form':form})

class ShippingAddressListView(LoginRequiredMixin, generic.ListView):
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_addresses.html'

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')

class ShippingAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.ListView):
    login_url = 'login'
    model = ShippingAddress
    form_class = ShippingForm
    template_name = 'update.html'
    succes_message = 'Direccion Actualizadad exitosamente'

    def get_succes_url(self):
        return reverse('shipping_address:shipping_addresses')