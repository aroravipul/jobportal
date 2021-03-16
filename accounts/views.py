from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages, auth
from employees.models import Employee
from employees.forms import EmployeeForm
from employers.models import Employer
from employers.forms import EmployerForm
from django.contrib.auth.models import User
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','jobportal.settings')

import django
django.setup()

def register_ee(request):
    return redirect('index')

def register_er(request):
    return redirect('index')
    
def register(request):

    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST, request.FILES)
        employer_form = EmployerForm(request.POST, request.FILES)
    
        
    # employee form check
        if employee_form.is_valid():
            password = employee_form.cleaned_data['password']
            password2 = employee_form.cleaned_data['confirm_password']
            uid = employee_form.cleaned_data['uid']
            #check if password matches
            if password==password2:
                employee_form.save()
                Employee.objects.get_or_create(uid=uid)
                user = User.objects.create_user(username=uid, password=password)
                #auth.login(request, user)
                return HttpResponseRedirect('login')

            else:
                messages.error(request, 'Passwords do not match')
                return redirect('index')
        #if employer_form.is_valid():
        #    employer_form.save()
        #    auth.login(request, user)
        return HttpResponseRedirect('index')

    #employer form check
        if employer_form.is_valid():
            password = employer_form.cleaned_data['password']
            password2 = employer_form.cleaned_data['confirm_password']
            firm_name = employer_form.cleaned_data['firm_name']
            #check if password matches
            if password==password2:
                if User.objects.filter(username=firm_name).exists():
                    messages.error(request, 'This Firm name is already being used')
                    return redirect('register')
                else:
                    employer_form.save()
                    Employer.objects.get_or_create(firm_name=firm_name)
                    User.objects.create_user(username=firm_name, password=password)

            else:
                messages.error(request, 'Passwords do not match')
                return redirect('register')
        #if employer_form.is_valid():
        #    employer_form.save()
        return HttpResponseRedirect('login')
    else:
        employee_form = EmployeeForm()
        employer_form = EmployerForm()
    return render(request, 'accounts/register.html', {'employee_form': employee_form, 'employer_form': employer_form})

def login(request):
    return render(request, 'accounts/login.html')

def logout(request):
    return redirect('index')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

