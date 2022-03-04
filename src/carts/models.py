from enum import unique
from itertools import product
from signal import signal
from django.db import models
from django.db.models.signals import pre_save
# Create your models here.
import uuid
from users.models import User
from products.models import Product

class Cart(models.Model):
    cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    subtotal = models.DecimalField(default= 0.0, max_digits= 8, decimal_places=2)
    total = models.DecimalField(default= 0.0, max_digits= 8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

def ser_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())

pre_save.connect(ser_cart_id, sender=Cart)