from django.db import models
#from employees.models import City
#from employees.models import Jobs

class Job(models.Model):
    job_name = models.CharField(max_length=20)
    job_category = models.CharField(max_length=20)
    def __str__(self):
        return self.job_name


class Employer(models.Model):
    firm_name = models.CharField(max_length=50)
    firm_category = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    requirement = models.ForeignKey(Job, on_delete=models.DO_NOTHING)
    no_of_requirments = models.IntegerField(default=1)
    salary_offered = models.IntegerField()
    SALARY_CHOICES = [
                        ('H','Hourly'),
                        ('D','Daily'),
                        ('M','Monthly') ]
    salary_frequency = models.CharField(max_length=20, choices=SALARY_CHOICES, default='Monthly')
    SHIFT_OFFERED_CHOICES = [('day','Day'),
                             ('night','Night')]
    shift_offered = models.CharField(max_length=10, choices=SHIFT_OFFERED_CHOICES, default='Day')
    match_otp = models.IntegerField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    discount = models.FloatField(default=0.0)
    SUBSCRIPTION_CHOICES = [('1month','999/One Month/10 Contacts'),
                            ('2month','1299/Two Month/10 Contacts')]
    subscription = models.CharField(max_length=50, choices=SUBSCRIPTION_CHOICES, default='999/One Month/10 Contacts')
    def __str__(self):
        return self.firm_name    



