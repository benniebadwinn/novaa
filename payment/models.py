from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# from django_countries.fields import CountryField
from django.contrib.auth.models import User



class Payment(models.Model):
    # country = CountryField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = PhoneNumberField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # Adjust max_digits as needed
    description = models.CharField(max_length=100, default='product/service purchased')
    type = models.CharField(default='MERCHANT', max_length=9)
    reference = models.CharField(max_length=6)
    paid = models.BooleanField(default=False)


    class Meta:
        verbose_name='Payment'
        verbose_name_plural = '1. Payment'

    def __str__(self):
    
        return str(self.first_name) + "/" + str(self.phone)

