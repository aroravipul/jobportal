from django import forms
from .models import Employee
from volunteers.models import Volunteer
from employers.models import Job

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ('is_published','match_otp', 'rojiroti_job_num', 'rojiroti_employer',
         'is_approved', 'create_date', 'discount', 'referral_points', 'rojiroti_referral_code',
        'subscription', )
        #widgets = {
         #           'uid': forms.TextInput(attrs={'placeholder': 'Aadhar Card'}),
         #           }
        labels = {
            'uid': ('Aadhar card number'),
            'job_preference1': ('First Job Preference'),
            'job_preference2': ('Second Job Preference'),
            'job_preference3': ('Third Job Preference'),
            'is_experienced': ('Are you experienced?'),
            'prev_work_exp': ('Your previous work experience(if any)'),
            'exp_salary': ('Expected Salary'),
            'exp_salary_frequency': ('Frequency of salary'),
            'pref_shift': ('Prefered Shift'),
            'pref_location': ('Prefered Location'),
            'uid_photo_front': ('Aadhar Card Photo (Front side)'),
            'uid_photo_back': ('Aadhar Card Photo (Back side)'),
            'self_photo': ('Your Photo'),
        }
    

    