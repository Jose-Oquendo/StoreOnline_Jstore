from django.contrib import admin

# Register your models here.
from shipping_address.models import ShippingAddress

admin.site.register(ShippingAddress)