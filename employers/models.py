from django.db import models
from datetime import datetime   
from accounts.models import Subscription_employer
#from employees.models import City
#from employees.models import Jobs

class Job(models.Model):
    job_name = models.CharField(max_length=20)
    job_category = models.CharField(max_length=20)
    def __str__(self):
        return self.job_name

class Employer(models.Model):
    firm_name = models.CharField(unique=True, max_length=50)
    firm_category = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    phone_verified = models.BooleanField(default=False)
    '''
    requirement = models.ForeignKey(Job, on_delete=models.DO_NOTHING)
    no_of_requirments = models.PositiveIntegerField(default=1)
    salary_offered = models.PositiveIntegerField()
    SALARY_CHOICES = [
                        ('H','Hourly'),
                        ('D','Daily'),
                        ('M','Monthly') ]
    salary_frequency = models.CharField(max_length=20, choices=SALARY_CHOICES, default='Monthly')
    SHIFT_OFFERED_CHOICES = [('day','Day'),
                             ('night','Night')]
    shift_offered = models.CharField(max_length=10, choices=SHIFT_OFFERED_CHOICES, default='Day')
    '''
    
    is_approved = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    discount = models.FloatField(default=0.0)
    #SUBSCRIPTION_CHOICES = [('1month','999/One Month/10 Contacts'),
    #                        ('2month','1299/Two Month/10 Contacts')]
    #subscription = models.CharField(max_length=50, choices=SUBSCRIPTION_CHOICES, default='999/One Month/10 Contacts')
    subscription_plan = models.ForeignKey(Subscription_employer, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    subscription_date = models.DateTimeField(default=datetime.now, blank=True)
    condition_agreed = models.BooleanField(default=False)
    def __str__(self):
        return self.firm_name    

class Ad(models.Model):
    firm = models.ForeignKey(Employer, on_delete=models.DO_NOTHING)
    requirement = models.ForeignKey(Job, on_delete=models.DO_NOTHING)
    no_of_requirments = models.PositiveIntegerField(default=1)
    salary_offered = models.PositiveIntegerField()
    SALARY_CHOICES = [
                        ('Hourly','Hourly'),
                        ('Daily','Daily'),
                        ('Monthly','Monthly') ]
    salary_frequency = models.CharField(max_length=20, choices=SALARY_CHOICES, default='Monthly')
    SHIFT_OFFERED_CHOICES = [('Day','Day'),
                             ('Night','Night'),
                             ('Any','Any')]
    shift_offered = models.CharField(max_length=10, choices=SHIFT_OFFERED_CHOICES, default='Day')
    create_date = models.DateTimeField(default=datetime.now, blank=True)
    is_published = models.BooleanField(default=False)
    match_otp = models.PositiveIntegerField(blank=True, null=True)
    def __str__(self):
        return self.requirement.job_name

