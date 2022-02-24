from django.contrib import admin

from products.models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    fields = ('tittle', 'description', 'price', 'image')
    list_display = ('__str__', 'slug', 'created_at')


admin.site.register(Product, ProductAdmin)

