from argparse import Namespace
from nturl2path import url2pathname
from django.urls import path
from billing_profiles import views

app_name = 'billing_profiles'

urlpatterns = [
    path('nuevo', views.create, name='create')
]
