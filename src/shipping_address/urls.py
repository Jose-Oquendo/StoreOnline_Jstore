from unicodedata import name
from django.urls import URLPattern, path

from shipping_address import views

app_name = 'shipping_address'

urlpatterns = [
    path('', views.ShippingAddressListView.as_view(), name='shipping_address'),
    path('nueva', views.create, name='create'),
    path('default/<int>:pk', views.default, name='default'),
    path('editar/<int>:pk', views.ShippingAddressUpdateView.as_view(), name='update'),
    path('eliminar/<int>:pk', views.ShippingAddressDeleteView.as_view(), name='delete'),
]