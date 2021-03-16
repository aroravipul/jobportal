from django.db import models
from datetime import datetime
from volunteers.models import Volunteer
from employers.models import Employer, Job

#class City(models.Model):
#    city_name = models.CharField(max_length=20)
#    postal_code = models.IntegerField()
#    def __str__(self):
#        return self.city_name


#class Qualification(models.Model):
#    qualification_name = models.CharField(max_length=50, default='none')
#    qualification_description = models.CharField(max_length=100, default='')
#    def __str__(self):
#        return self.qualification_name

class Employee(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.DO_NOTHING)
    uid = models.CharField(primary_key=True, max_length=20)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    GENDER_CHOICES = [
                        ('Male','Male'),
                        ('Female','Female'),
                        ('Others','Others')    ]
    SALARY_CHOICES = [
                        ('Hourly','Hourly'),
                        ('Daily','Daily'),
                        ('Monthly','Monthly') ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=100)
    city = models.CharField(max_length=50)   # not from city table
    job_preference1 = models.ForeignKey(Job, on_delete=models.DO_NOTHING, related_name = 'jp1')  # from jobs table
    job_preference2 = models.ForeignKey(Job, on_delete=models.DO_NOTHING, blank=True, null=True, related_name = 'jp2')  # from jobs table
    job_preference3 = models.ForeignKey(Job, on_delete=models.DO_NOTHING, blank=True, null=True, related_name = 'jp3')  # from jobs table
    is_experienced = models.BooleanField(default=False)
    prev_work_exp = models.CharField(max_length=100) # from jobs table
    qualification = models.CharField(max_length=100) #ForeignKey(Qualification, on_delete=models.DO_NOTHING) # from qualification table
    exp_salary = models.IntegerField()  # from salary table, currently fixed in options
    exp_salary_frequency = models.CharField(max_length=20, choices=SALARY_CHOICES, default='Monthly')
    SHIFT_OFFERED_CHOICES = [('day','Day'),
                             ('night','Night'),
                             ('any','Any')]
    pref_shift = models.CharField(max_length=20, choices=SHIFT_OFFERED_CHOICES, default='Day') 
    pref_location = models.CharField(max_length=50) # from city table, currently fixed to Saharanpur
    #comments = models.CharField(max_length=200) 
    uid_photo_front = models.ImageField(upload_to='photos/%Y/%m/%d/')
    uid_photo_back = models.ImageField(upload_to='photos/%Y/%m/%d/')
    self_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True, default='photos/default.png')
    create_date = models.DateTimeField(default=datetime.now, blank=True)
    is_approved = models.BooleanField(default=False)
    match_otp = models.IntegerField(blank=True, null=True)
    rojiroti_job_num = models.IntegerField(default=0)
    rojiroti_employer = models.ForeignKey(Employer, on_delete=models.DO_NOTHING, null=True, blank=True) # from employer table
    rojiroti_referral_code = models.CharField(blank=True, max_length=8, null=True)
    is_published = models.BooleanField(default=True)
    discount = models.FloatField(default=0.0)
    SUBSCRIPTION_CHOICES = [('1st_time','150/First time'),
                            ('return_user','250/Returned user')]
    subscription = models.CharField(max_length=50, choices=SUBSCRIPTION_CHOICES, default='150/First time')
    referral_points = models.IntegerField(default=0)
    def __str__(self):
        return self.uid


     