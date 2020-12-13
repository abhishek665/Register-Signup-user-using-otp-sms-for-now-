from django.db import models
import datetime
from django.core.validators import RegexValidator


# Create your models here.

def profile_upload(instance, filename):
    return '{0}/{1}'.format(instance.contact, filename)


class MyUser(models.Model):
    contact = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, default="")
    address = models.CharField(max_length=500, default="")
    level = models.IntegerField(default=0)
    join_date = models.DateTimeField(auto_now_add=True)
    interest = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return str(self.contact)



class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Enter Valid number")
    contact = models.CharField(default="", max_length=17, unique=True)
    otp = models.IntegerField(blank=True, null=True)
    count = models.IntegerField(default=0, help_text="number of OTP sent")
    date = models.DateTimeField(auto_now_add=True)
    validated = models.BooleanField(default=False, help_text="If its True user is validated")

    def __str__(self):
        return str(self.contact) + 'is sent' + str(self.otp)