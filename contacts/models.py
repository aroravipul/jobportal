from django.db import models
from datetime import datetime
from employers.models import Ad


class Employer_to_employee(models.Model):
    employee_id = models.CharField(max_length=20)
    firm_name = models.CharField(max_length=100)
    employer_ad = models.ForeignKey(Ad, on_delete=models.DO_NOTHING, default='')
    employee_phone = models.CharField(max_length=10, blank= True)
    contact_date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.employee_id

class Employee_to_employer(models.Model):
    ad_id = models.ForeignKey(Ad, on_delete=models.DO_NOTHING, default='')
    employee_id = models.CharField(max_length=20)
    employee_fullname = models.CharField(max_length=100, default='')
    employer_phone = models.CharField(max_length=10, blank=True)
    contact_date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.ad_id.requirement.job_name
