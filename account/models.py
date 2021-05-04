from django.contrib.auth.models import AbstractUser
from django.db import models
#from phone_field import PhoneField
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField



class MembershipType(models.Model):
    title = models.CharField(max_length=150)
    price = models.IntegerField()

    def __str__(self):
        return str(self.title) + ' | ' + str(self.price)


class User(AbstractUser):
    country = CountryField(null=True,default='Nepal')
    is_verified = models.BooleanField(default=False)
    is_otp_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    phone = PhoneNumberField(
        blank=True, help_text='Contact phone number', unique=True)
    membership = models.ForeignKey(MembershipType,on_delete=models.CASCADE,null=True,blank=True)
    auth_token = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.username)

    @property
    def f_name(self):
        s = str(self.first_name) + ' ' + str(self.last_name)
        return s

    @property
    def astatus(self):
        if self.is_active:
            return "Active"
        else:
            return "Suspended"      

    @property
    def mstatus(self):
        if self.is_verified:
            return "Verified"
        else:
            return "Not Verified"                 
