from django.db import models
from django.core.validators import RegexValidator
'''from django.contrib.auth.models import AbstractUser
'''
# for adding custom fields in User
class User_category(models.Model):
   username = models.CharField(unique=True, max_length=12)
   #is_employer = models.BooleanField(default=True)

class Subscription_employee(models.Model):
   package_name = models.CharField(max_length=20)
   price = models.PositiveIntegerField()
   validity = models.CharField(max_length=50, default="Month")
   feature1 = models.CharField(max_length=200, blank=True)
   feature2 = models.CharField(max_length=200, blank=True)
   feature3 = models.CharField(max_length=200, blank=True)
   feature4 = models.CharField(max_length=200, blank=True)
   feature5 = models.CharField(max_length=200, blank=True)
   feature6 = models.CharField(max_length=200, blank=True)
   feature7 = models.CharField(max_length=200, blank=True)
   feature8 = models.CharField(max_length=200, blank=True)
   feature9 = models.CharField(max_length=200, blank=True)
   feature10 = models.CharField(max_length=200, blank=True)
   is_active = models.BooleanField(default=True)
   def __str__(self):
        return self.package_name

class Subscription_employer(models.Model):
   package_name = models.CharField(max_length=20)
   price = models.IntegerField()
   validity = models.CharField(max_length=50, default="Month")
   feature1 = models.CharField(max_length=200, blank=True)
   feature2 = models.CharField(max_length=200, blank=True)
   feature3 = models.CharField(max_length=200, blank=True)
   feature4 = models.CharField(max_length=200, blank=True)
   feature5 = models.CharField(max_length=200, blank=True)
   feature6 = models.CharField(max_length=200, blank=True)
   feature7 = models.CharField(max_length=200, blank=True)
   feature8 = models.CharField(max_length=200, blank=True)
   feature9 = models.CharField(max_length=200, blank=True)
   feature10 = models.CharField(max_length=200, blank=True)
   is_active = models.BooleanField(default=True)
   def __str__(self):
        return self.package_name

class PhoneOTP(models.Model):
 
    phone_regex = RegexValidator( regex = r'^\+?1?\d{9,10}$', message ="Phone number must be entered in the format +919999999999. Up to 14 digits allowed.")
    phone       = models.CharField(validators =[phone_regex], max_length=17, unique = True)
    otp         = models.CharField(max_length=9, blank = True, null=True)
    count       = models.IntegerField(default=0, help_text = 'Number of otp_sent')
    validated   = models.BooleanField(default = False, help_text = 'If it is true, that means user have validate otp correctly in second API')
    otp_session_id = models.CharField(max_length=120, null=True, default = "")
    username    = models.CharField(max_length=50, blank = True, null = True, default = None )
    #email       = models.CharField(max_length=50, null = True, blank = True, default = None) 
    #password    = models.CharField(max_length=100, null = True, blank = True, default = None) 

    

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)    

