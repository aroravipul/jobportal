from django.db import models
from datetime import datetime

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    self_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    designation = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    #no_of_registrations = models.IntegerField(default=0)
    hire_date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.name
