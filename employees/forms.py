from django import forms
from .models import Employee
from volunteers.models import Volunteer
from employers.models import Job

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ('is_published','match_otp', 'rojiroti_job_num', 'rojiroti_employer', 'is_approved', 'create_date', 'discount', 'referral_points')
        #widgets = {
         #           'uid': forms.TextInput(attrs={'placeholder': 'Aadhar Card'}),
         #           }
        labels = {
            'uid': ('Aadhar card number'),
        }
    password = forms.CharField(min_length=8, required=True)
    confirm_password = forms.CharField(min_length=8, required=True)

    