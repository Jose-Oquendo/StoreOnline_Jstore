from unicodedata import name
from django.contrib import admin
from django.urls import path, include

from products import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='products'),
]
