from django.db import models
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


