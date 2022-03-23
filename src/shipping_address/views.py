
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from shipping_address.forms import ShippingForm
from shipping_address.models import ShippingAddress
from users.models import User

@login_required(login_url='login')
def create(request):
    form = ShippingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        shipping_address = form.save(commit=False)
        shipping_address.user = request.user
        shipping_address.default = not request.user.has_shipping_address()
       
        ShippingAddress.objects.filter(user=request.user).exists()
        shipping_address.save()
       
        messages.success(request,'Direccion creada con exito')
        return redirect('shipping_address:shipping_address')
    
    return render(request, 'create.html', {'form':form})

@login_required(login_url='login')
def default(request, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk = pk)
    if request.user.id != shipping_address.user_id:
        return redirect('cart:carts')

    if request.user.has_shipping_address():
        request.user.shipping_address.update_default()

    shipping_address.update_default(True)
    return redirect('shipping_address:shipping_address')

class ShippingAddressListView(LoginRequiredMixin, generic.ListView):
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_addresses.html'

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')

class ShippingAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    login_url = 'login'
    models = ShippingAddress
    form_class = ShippingForm
    template_name = 'update.html'
    succes_message = 'Direccion Actualizadad exitosamente'

    def get_success_url(self):
        return reverse('shipping_address:shipping_address')

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')
        return super(ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)

    #defino el query set
    def get_queryset(self):
      return ShippingAddress.objects.order_by('id')

class ShippingAddressDeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = 'login'
    models = ShippingAddress
    template_name = 'delete.html'
    success_url = reverse_lazy('shipping_address:shipping_address')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().default:
            return redirect('shipping_address:shipping_address')
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')
        return super(ShippingAddressDeleteView, self).dispatch(request, *args, **kwargs)

    #defino el query set
    def get_queryset(self):
      return ShippingAddress.objects.order_by('id')