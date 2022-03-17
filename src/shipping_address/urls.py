from django.urls import URLPattern, path

from shipping_address import views

app_name = 'shipping_address'

URLPattern = [
    path('', views.ShippingAddressListView.as_view(), name='shipping_address'),
]