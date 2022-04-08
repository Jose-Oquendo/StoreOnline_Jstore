from unicodedata import name
from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.order, name='order'),
    path('direccion', views.address, name='address'),
    path('seleccionar/direccion', views.select_address, name="select_address"),
    path('seleccionar/direccion/<int:pk>', views.check_address, name="check_address"),
    path('confirmacion', views.confirm, name='confirm'),
    path('pago', views.to_pay, name="pay"),
    path('cargo', views.charge, name="charge"),
    path('cancelar', views.cancel, name='cancel'),
    path('completar', views.complete, name='complete'),
    path('completados', views.OrderListView.as_view(), name='completed'),
]