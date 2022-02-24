from optparse import TitledHelpFormatter
from django.db import models

from django.utils.text import slugify
from django.db.models.signals import pre_save
import uuid

# Create your models here.
class Product(models.Model):
    tittle = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    slug = models.SlugField(null=False, blank=False, unique=True)
    image = models.ImageField(upload_to='products/', null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    '''def save(self, *args, **kwargs):
        self.slug = slugify(self.tittle)
        super(Product, self).save(*args, **kwargs)'''

    def __str__(self):
        return(self.tittle)

def set_slug(sender, instance, *args, **kwargs):
    if instance.tittle and not instance.slug:
        slug = slugify(instance.tittle)
        while Product.objects.filter(slug = slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.tittle, str(uuid.uuid4()))[:8]
            )
    instance.slug = slug
    
pre_save.connect(set_slug, sender = Product)