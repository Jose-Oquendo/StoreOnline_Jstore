from email.policy import default
from pickle import FALSE
from django.db import models

# Create your models here.
from users.models import User

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    line1 =  models.CharField(max_length= 200)
    line2 = models.CharField(max_length= 200 ,blank=True)
    city = models.CharField(max_length= 100)
    state = models.CharField(max_length= 100)
    country =   models.CharField(max_length= 50)
    reference = models.CharField(max_length= 300)
    postal_code =  models.CharField(max_length=10 , null=False, blank=True) 
    default = models.BooleanField(default = False)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.postal_code

    def update_default(self, default=False):
        self.default = default
        self.save()

    def address(self):
        return '{} - {} - {}'.format(self.city, self.state, self.country)

