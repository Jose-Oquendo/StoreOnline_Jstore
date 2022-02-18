from optparse import TitledHelpFormatter
from django.db import models

# Create your models here.
class Product(models.Model):
    tittle = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    