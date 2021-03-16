from django import forms
from .models import Employer, Job


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        exclude = ('is_published','match_otp', 'is_approved', 'create_date', 'discount')
        #widgets = {
         #           'uid': forms.TextInput(attrs={'placeholder': 'Aadhar Card'}),
         #           }
        #labels = {
        #    'uid': ('Aadhar card number'),
        #}
    password = forms.CharField(min_length=8, required=True)
    confirm_password = forms.CharField(min_length=8, required=True)

    