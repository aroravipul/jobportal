from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics
from django.contrib import messages, auth
from employees.models import Employee
from employees.forms import EmployeeForm
from employers.models import Employer, Job, Ad
from volunteers.models import Volunteer
from .models import User_category, Subscription_employee, Subscription_employer, PhoneOTP
from employers.forms import EmployerForm
from django.contrib.auth.models import User
from contacts.models import Employee_to_employer, Employer_to_employee
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','jobportal.settings')
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import random
import django
import json
import ast
import http.client
django.setup()
conn = http.client.HTTPConnection("2factor.in")


def register_ee(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        uid = request.POST['uid']
        password = request.POST['password']
        password2 = request.POST['password2']
    # if password matches
        if password == password2:
        # if user already exists
            if User.objects.filter(username=uid).exists():
                messages.error(request, 'That Aadhar card is already registered, please login!')
                return redirect('login')
            else:
                user = User.objects.create_user(username=uid, password=password, 
                first_name=first_name, last_name=last_name)

                employee_user = User_category(username=uid)
                employee_user.save()
                #login after user creation
                auth.login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('profile_ee')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

    return redirect('index')

def register_er(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        firmname = request.POST['firmname']
        password = request.POST['password']
        password2 = request.POST['password2']
    # if password matches
        if password == password2:
        # if user already exists
            if User.objects.filter(username=firmname).exists():
                messages.error(request, 'That Firm is already registered, please login!')
                return redirect('login')
            else:
                user = User.objects.create_user(username=firmname, password=password, 
                first_name=first_name, last_name=last_name)
                #login after user creation
                auth.login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('profile_er')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

    return redirect('index')

def register(request):
    return render(request, 'accounts/register.html')
'''
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
        employer_form = EmployerForm()'''
    #return render(request, 'accounts/register.html', {'employee_form': employee_form, 'employer_form': employer_form})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')

def dashboard(request):
    if request.user.username.isdigit():
        is_employee = "True"
        print(is_employee)
        contacts_for_u = Employer_to_employee.objects.order_by('-contact_date').filter(employee_id=request.user.username)
        contacts_by_u = Employee_to_employer.objects.order_by('-contact_date').filter(employee_id=request.user.username)
        employee_otp = Employee.objects.get(uid=request.user.username)
        print(employee_otp.match_otp)
        context = {
            'is_employee': is_employee,
            'contacts_for_u': contacts_for_u,
            'contacts_by_u': contacts_by_u,
            'employee_otp' : employee_otp            
        }
    else:
        is_employee = "False"
        print(is_employee)
        employer_id = Employer.objects.values_list('id', flat=True).filter(firm_name=request.user.username)
        ads_by_user = Ad.objects.values_list('id', flat=True).filter(firm=employer_id.first())
        print(ads_by_user)
        contacts_by_u = Employer_to_employee.objects.order_by('-contact_date').filter(firm_name=request.user.username)
        print(contacts_by_u)
        contacts_for_u = []
        for ad in ads_by_user:
            print(ad)
            contacts_for_u = Employee_to_employer.objects.order_by('-contact_date').filter(ad_id=ad)
            #if contact_for_u:
            #    contacts_for_u.append(contact_for_u)        
        print(contacts_for_u)
        #print(employer_id.first())
        ads = Ad.objects.all().filter(firm_id = employer_id.first())
        print(ads)
        #ads = Ad.objects.get(id=1)
        #ads = contacts_for_u
        
        context = {
            'is_employee': is_employee,
            'contacts_for_u': contacts_for_u,
            'contacts_by_u': contacts_by_u,
            'ads': ads
        }
    return render(request, 'accounts/dashboard.html', context)

def profile(request, name):
    if name.isdigit():
        print("employee")
        return profile_ee(request)
    else:
        print("employer")
        return profile_er(request)


def profile_ee(request):
    employee = Employee.objects.values_list('uid', flat=True)
    #print(employee)
    current_user = request.user.username
    #print(current_user)
    if current_user in employee:
        if request.method == 'POST': # and request.FILES['uid_photo_front'] and request.FILES['uid_photo_back'] and request.FILES['self_photo']:
        #save attachment Aadhar front 
            print('1')
            '''if request.FILES['uid_photo_front']:
                print('2')
                uid_photo_front = request.FILES['uid_photo_front']
                fs1 = FileSystemStorage()
                filename1 = fs1.save(uid_photo_front.name, uid_photo_front)
                uploaded_file_url1 = fs.url(filename1)
            else:
                print('3')
                uid_photo_front = request.POST.get('uid_photo_front')
            #save attachment Aadhar back 
            if (request.FILES['uid_photo_back']):
                print('4')
                uid_photo_back = request.FILES['uid_photo_back']
                fs2 = FileSystemStorage()
                filename2 = fs2.save(uid_photo_back.name, uid_photo_back)
                uploaded_file_url2 = fs.url(filename2)
            else:
                uid_photo_back = request.POST.get('uid_photo_back')

            #save attachment self photo 
            if (request.FILES['self_photo']):
                self_photo = request.FILES['self_photo']
                fs3 = FileSystemStorage()
                filename3 = fs3.save(self_photo.name, self_photo)
                uploaded_file_url3 = fs.url(filename3)
            else:
                self_photo = request.POST.get('self_photo')
            '''
            #get field inputs
            volunteer = request.POST.get('volunteer')
            uid = request.POST.get('uid')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            city = request.POST.get('city')
            phone = request.POST.get('phone')
            job_preference1 = request.POST.get('job_preference1')
            job_preference2 = request.POST.get('job_preference2')
            job_preference3 = request.POST.get('job_preference3')
            is_experienced = request.POST.get('is_experienced')
            prev_work_exp = request.POST.get('prev_work_exp')
            qualification = request.POST.get('qualification')
            exp_salary = request.POST.get('exp_salary')
            exp_salary_frequency = request.POST.get('exp_salary_frequency')
            pref_shift = request.POST.get('pref_shift')
            pref_location = request.POST.get('pref_location')
            #uid_photo_front = request.POST.get('uid_photo_front')
            #uid_photo_back = request.POST.get('uid_photo_back')
            #self_photo = request.POST.get('self_photo')
            # Check Age if the employee
            get_employee = Employee.objects.get(uid=current_user)
            #volunteer = request.POST['volunteer']
            volunteer_id = Volunteer.objects.get(name=volunteer)
            job1 = Job.objects.get(job_name=job_preference1)
            job2 = Job.objects.get(job_name=job_preference2)
            job3 = Job.objects.get(job_name=job_preference3)
            get_employee.volunteer = volunteer_id
            get_employee.first_name = first_name
            get_employee.last_name = last_name 
            get_employee.age = age
            get_employee.gender = gender
            get_employee.city = city
            get_employee.phone = phone
            get_employee.job_preference1 = job1
            get_employee.job_preference2 = job2
            get_employee.job_preference3 = job3
            get_employee.is_experienced = is_experienced
            get_employee.prev_work_exp = prev_work_exp
            get_employee.qualification = qualification
            get_employee.exp_salary = exp_salary
            get_employee.exp_salary_frequency = exp_salary_frequency
            get_employee.pref_shift = pref_shift
            get_employee.pref_location = pref_location
            '''if uid_photo_front:
                get_employee.uid_photo_front = uid_photo_front
            if uid_photo_back:
                get_employee.uid_photo_back = uid_photo_back
            if self_photo:
                get_employee.self_photo = self_photo
            '''
            get_employee.save()
            messages.success(request, 'Your profile is updated successfully')
            return HttpResponseRedirect('dashboard')
        else:
            employee = Employee.objects.get(uid=current_user)
            print(employee.is_experienced)
            volunteer_list = Volunteer.objects.all()
            job_list = Job.objects.all()
            #employee_form = EmployeeForm()
            context = {
            #    'employee_form': employee_form,
                'salary_choices': Employee.SALARY_CHOICES,
                'gender_choices': Employee.GENDER_CHOICES,
                'qualification_choices': Employee.QUALIFICATION_CHOICES,
                'shift_choices': Employee.SHIFT_OFFERED_CHOICES,
                'volunteers': volunteer_list,
                'jobs': job_list,
                'employee' : employee
                }
            
            return render(request, 'accounts/profile_ee.html', context)
    else:
        if request.method == 'POST' and request.FILES['uid_photo_front'] and request.FILES['uid_photo_back'] and request.FILES['self_photo']:
        #save attachment Aadhar front 
            print('1')
            if (request.FILES['uid_photo_front']):
                print('2')
                uid_photo_front = request.FILES['uid_photo_front']
                fs1 = FileSystemStorage()
                filename1 = fs1.save(uid_photo_front.name, uid_photo_front)
                uploaded_file_url1 = fs1.url(filename1)
            else:
                print('3')
                uid_photo_front = request.POST.get('uid_photo_front')
            #save attachment Aadhar back 
            if (request.FILES['uid_photo_back']):
                print('4')
                uid_photo_back = request.FILES['uid_photo_back']
                fs2 = FileSystemStorage()
                filename2 = fs2.save(uid_photo_back.name, uid_photo_back)
                uploaded_file_url2 = fs2.url(filename2)
            else:
                uid_photo_back = request.POST.get('uid_photo_back')

            #save attachment self photo 
            if (request.FILES['self_photo']):
                self_photo = request.FILES['self_photo']
                fs3 = FileSystemStorage()
                filename3 = fs3.save(self_photo.name, self_photo)
                uploaded_file_url3 = fs3.url(filename3)
            else:
                self_photo = request.POST.get('self_photo')
            
            #get field inputs
            volunteer = request.POST.get('volunteer')
            uid = request.POST.get('uid')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            city = request.POST.get('city')
            phone = request.POST.get('phone')
            job_preference1 = request.POST.get('job_preference1')
            job_preference2 = request.POST.get('job_preference2')
            job_preference3 = request.POST.get('job_preference3')
            is_experienced = request.POST.get('is_experienced')
            prev_work_exp = request.POST.get('prev_work_exp')
            qualification = request.POST.get('qualification')
            exp_salary = request.POST.get('exp_salary')
            exp_salary_frequency = request.POST.get('exp_salary_frequency')
            pref_shift = request.POST.get('pref_shift')
            pref_location = request.POST.get('pref_location')
            condition_agreed = request.POST.get('condition_agreed', False)
            #uid_photo_front = request.POST.get('uid_photo_front')
            #uid_photo_back = request.POST.get('uid_photo_back')
            #self_photo = request.POST.get('self_photo')
            # Check Age if the employee
            age=int(age)
            if age<18:
                messages.error(request, 'You are not eligible to apply as per the Child Labour Law since you are less than 18 years old.')
                print(request)
                
                return redirect('index')

            else:
                volunteer_id = Volunteer.objects.get(name=volunteer)
                job1 = Job.objects.get(job_name=job_preference1)
                job2 = Job.objects.get(job_name=job_preference2)
                job3 = Job.objects.get(job_name=job_preference3)

                new_employee = Employee(volunteer=volunteer_id, uid = uid,
                first_name = first_name,
                last_name = last_name,
                age = age,
                gender = gender,
                city = city,
                phone = phone,
                job_preference1 = job1,
                job_preference2 = job2,
                job_preference3 = job3,
                is_experienced = is_experienced,
                prev_work_exp = prev_work_exp,
                qualification = qualification,
                exp_salary = exp_salary,
                exp_salary_frequency = exp_salary_frequency,
                pref_shift = pref_shift,
                pref_location = pref_location,
                uid_photo_front = uid_photo_front,
                uid_photo_back = uid_photo_back,
                self_photo = self_photo,
                condition_agreed= condition_agreed)
                new_employee.save()

                context = {
                'current_user' : current_user,
                'phone' : phone
                }

                messages.success(request, 'Your profile is updated successfully')
                return render( request, 'accounts/validate_phone.html', context)
        else:
            volunteer_list = Volunteer.objects.all()
            job_list = Job.objects.all()
            context = {
            #    'employee_form': employee_form,
                'salary_choices': Employee.SALARY_CHOICES,
                'gender_choices': Employee.GENDER_CHOICES,
                'qualification_choices': Employee.QUALIFICATION_CHOICES,
                'shift_choices': Employee.SHIFT_OFFERED_CHOICES,
                'volunteers': volunteer_list,
                'jobs': job_list,
                }
            return render(request, 'accounts/profile_ee.html', context)
##################################################################
'''
    if request.method == 'POST': # and request.FILES['uid_photo_front'] and request.FILES['uid_photo_back'] and request.FILES['self_photo']:
        #save attachment Aadhar front 
        print('1')
        if (request.FILES['uid_photo_front']):
            print('2')
            uid_photo_front = request.FILES['uid_photo_front']
            fs1 = FileSystemStorage()
            filename1 = fs1.save(uid_photo_front.name, uid_photo_front)
            uploaded_file_url1 = fs.url(filename1)
        else:
            print('3')
            uid_photo_front = request.POST.get('uid_photo_front')
        #save attachment Aadhar back 
        if (request.FILES['uid_photo_back']):
            print('4')
            uid_photo_back = request.FILES['uid_photo_back']
            fs2 = FileSystemStorage()
            filename2 = fs2.save(uid_photo_back.name, uid_photo_back)
            uploaded_file_url2 = fs.url(filename2)
        else:
            uid_photo_back = request.POST.get('uid_photo_back')

        #save attachment self photo 
        if (request.FILES['self_photo']):
            self_photo = request.FILES['self_photo']
            fs3 = FileSystemStorage()
            filename3 = fs3.save(self_photo.name, self_photo)
            uploaded_file_url3 = fs.url(filename3)
        else:
            self_photo = request.POST.get('self_photo')
        
        #get field inputs
        volunteer = request.POST.get('volunteer')
        uid = request.POST.get('uid')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        job_preference1 = request.POST.get('job_preference1')
        job_preference2 = request.POST.get('job_preference2')
        job_preference3 = request.POST.get('job_preference3')
        is_experienced = request.POST.get('is_experienced')
        prev_work_exp = request.POST.get('prev_work_exp')
        qualification = request.POST.get('qualification')
        exp_salary = request.POST.get('exp_salary')
        exp_salary_frequency = request.POST.get('exp_salary_frequency')
        pref_shift = request.POST.get('pref_shift')
        pref_location = request.POST.get('pref_location')
        #uid_photo_front = request.POST.get('uid_photo_front')
        #uid_photo_back = request.POST.get('uid_photo_back')
        #self_photo = request.POST.get('self_photo')
        # Check Age if the employee
        
        
        if current_user in employee:
            get_employee = Employee.objects.get(uid=current_user)
            #volunteer = request.POST['volunteer']
            volunteer_id = Volunteer.objects.get(name=volunteer)
            job1 = Job.objects.get(job_name=job_preference1)
            job2 = Job.objects.get(job_name=job_preference2)
            job3 = Job.objects.get(job_name=job_preference3)
            get_employee.volunteer = volunteer_id
            get_employee.first_name = first_name
            get_employee.last_name = last_name 
            get_employee.age = age
            get_employee.gender = gender
            get_employee.city = city
            get_employee.phone = phone
            get_employee.job_preference1 = job1
            get_employee.job_preference2 = job2
            get_employee.job_preference3 = job3
            get_employee.is_experienced = is_experienced
            get_employee.prev_work_exp = prev_work_exp
            get_employee.qualification = qualification
            get_employee.exp_salary = exp_salary
            get_employee.exp_salary_frequency = exp_salary_frequency
            get_employee.pref_shift = pref_shift
            get_employee.pref_location = pref_location
            if uid_photo_front:
                get_employee.uid_photo_front = uid_photo_front
            if uid_photo_back:
                get_employee.uid_photo_back = uid_photo_back
            if self_photo:
                get_employee.self_photo = self_photo
            get_employee.save()
            messages.success(request, 'Your profile is updated successfully')
            return HttpResponseRedirect('dashboard')
        
        else:
            age=int(age)
            if age<18:
                messages.error(request, 'You are not eligible to apply as per the Child Labour Law since you are less than 18 years old.')
                print(request)
                
                return redirect('index')

            else:
                volunteer_id = Volunteer.objects.get(name=volunteer)
                job1 = Job.objects.get(job_name=job_preference1)
                job2 = Job.objects.get(job_name=job_preference2)
                job3 = Job.objects.get(job_name=job_preference3)

                new_employee = Employee(volunteer=volunteer_id, uid = uid,
                first_name = first_name,
                last_name = last_name,
                age = age,
                gender = gender,
                city = city,
                phone = phone,
                job_preference1 = job1,
                job_preference2 = job2,
                job_preference3 = job3,
                is_experienced = is_experienced,
                prev_work_exp = prev_work_exp,
                qualification = qualification,
                exp_salary = exp_salary,
                exp_salary_frequency = exp_salary_frequency,
                pref_shift = pref_shift,
                pref_location = pref_location,
                uid_photo_front = uid_photo_front,
                uid_photo_back = uid_photo_back,
                self_photo = self_photo)
                new_employee.save()

                messages.success(request, 'Your profile is updated successfully')
                return HttpResponseRedirect('subscription')
    else:
        if current_user in employee:
            print('True')
            employee = Employee.objects.get(uid=current_user)
            print(employee.is_experienced)
            volunteer_list = Volunteer.objects.all()
            job_list = Job.objects.all()
            #employee_form = EmployeeForm()
            context = {
            #    'employee_form': employee_form,
                'salary_choices': Employee.SALARY_CHOICES,
                'gender_choices': Employee.GENDER_CHOICES,
                'qualification_choices': Employee.QUALIFICATION_CHOICES,
                'shift_choices': Employee.SHIFT_OFFERED_CHOICES,
                'volunteers': volunteer_list,
                'jobs': job_list,
                'employee' : employee
                }
            
            return render(request, 'accounts/profile_ee.html', context)
        else:
            #print('false')
            #employee_form = EmployeeForm()
            volunteer_list = Volunteer.objects.all()
            job_list = Job.objects.all()
            context = {
            #    'employee_form': employee_form,
                'salary_choices': Employee.SALARY_CHOICES,
                'gender_choices': Employee.GENDER_CHOICES,
                'qualification_choices': Employee.QUALIFICATION_CHOICES,
                'shift_choices': Employee.SHIFT_OFFERED_CHOICES,
                'volunteers': volunteer_list,
                'jobs': job_list,
                }
            return render(request, 'accounts/profile_ee.html', context)
'''
def profile_er(request):
    '''if request.method == 'GET':
        employer = Employer.objects.filter(firm_name=id)
        if employer:
            context = {
                        'employer' : employer
                      }
        
        return render(request, 'accounts/profile_er.html', context)
    '''
    employer = Employer.objects.values_list('firm_name', flat=True)
    current_user = request.user.username
    if request.method == 'POST':
        firm_name = request.POST['firm_name']
        category = request.POST['category']
        fullname = request.POST['fullname'] 
        address = request.POST['address']
        city = request.POST['city']
        phone = request.POST['phone']
        condition_agreed = request.POST['condition_agreed']

        if current_user in employer:
            get_employer = Employer.objects.get(firm_name=current_user)
            get_employer.firm_category=category
            get_employer.full_name=fullname
            get_employer.address=address
            get_employer.city=city
            get_employer.phone=phone
            get_employer.condition_agreed=condition_agreed
            get_employer.save()
            messages.success(request, 'Your profile is updated successfully')
            return HttpResponseRedirect('dashboard')

        else:
            new_employer = Employer(firm_name=current_user, firm_category=category, 
            full_name=fullname, address=address, city=city, phone=phone, condition_agreed=condition_agreed)
            new_employer.save()

            context = {
                'current_user' : current_user,
                'phone' : phone
            }

            messages.success(request, 'Your profile is updated successfully')
            return render( request, 'accounts/validate_phone.html', context)
    else:
        #if request.user.username in Employer.objects.values('firm_name', flat=True):
        
        print(employer)
        
        print(current_user)
        if current_user in employer:
            employer = Employer.objects.get(firm_name=current_user)
            context = {
                     'employer' : employer
                      }
            return render(request, 'accounts/profile_er.html', context)
        else:
            return render(request, 'accounts/profile_er.html')
        #else:
        #    return render(request, 'accounts/profile_er.html')
        
        #return render(request, 'accounts/profile_er.html')
    #return redirect('dashboard')

def subscription(request):
    #if employee
    current_user = request.user.username
    if current_user.isdigit():
        print("Employee")
        plans = Subscription_employee.objects.filter(is_active=True)
        
        context = {
            'plans': plans
        }
        
        return render(request, 'accounts/subscription.html', context)
    #if employer
    else:
        print("Employer")
        plans = Subscription_employer.objects.filter(is_active=True)
        
        context = {
            'plans': plans
        }
        
        return render(request, 'accounts/subscription.html', context)

def generate_otp(request, id):
    if request.user.username.isdigit():
        # employee it is. generate otp and save in the profile
        otp = random.randint(100000,999999)
        otp_ee = Employee.objects.get(uid=id)
        otp_ee.match_otp=otp
        otp_ee.save()
        messages.success(request, 'OTP generated successfully')
        return redirect('dashboard')

    else:
        # employer it is. take input and complete employee hiring
        messages.success(request, 'OTP cannot be generated')
        return HttpResponseRedirect('dashboard')

def match_otp(request, id, ad_id):
    if request.user.username.isdigit():
        messages.success(request, 'OTP cannot be generated')
        return HttpResponseRedirect('dashboard')
    
    else:
        otp = request.POST.get('otp')
        otp_ee = Employee.objects.get(uid=id, match_otp=otp)
        ad = Ad.objects.get(id=ad_id)
        if otp_ee:
            otp_ee.is_published = False
            otp_ee.rojiroti_job_num = otp_ee.rojiroti_job_num+1
            otp_ee.save()
            print(ad.no_of_requirments)
            ad.no_of_requirments = ad.no_of_requirments-1
            if ad.no_of_requirments==0:
                ad.is_published = False
            ad.save()
            print(ad.no_of_requirments)
            messages.success(request, "OTP matched. Congratulations, you have hired an employee")
            return redirect('dashboard')

        else:
            messages.error(request, "incorrect OTP. Please try again.")
            return redirect('dashboard')

#class ValidatePhoneSendOTP(APIView):

def ValidatePhoneSendOTP(request, *args, **kwargs):
    current_user = request.user.username
    if current_user.isdigit():
        user_data = Employee.objects.filter(uid=current_user)
        phone = user_data.first().phone
    else:
        user_data = Employer.objects.filter(firm_name=current_user)
        phone = user_data.first().phone
    context={
        'current_user': current_user,
        'phone' : phone
    }  
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        #password = request.POST.get('password', False)
        username = request.POST.get('username', False)
        #email    = request.POST.get('email', False)

        if phone_number:
            phone = str(phone_number)
            user = Employer.objects.filter(phone__iexact = phone)
            print(user)
            if user:

                if user.first().phone_verified == True:
                    messages.error(request, 'Phone number already verified' )
                    return render(request, 'pages/index.html')
                    #return Response({
                    #    'status' : False,
                    #    'detail' : 'Phone number already verified'
                    #})

                else:
                    key = send_otp(phone)
                    if key:
                        old = PhoneOTP.objects.filter(phone__iexact = phone)
                        if old.exists():
                            old = old.first()
                            count = old.count
                            if count > 10:
                                messages.error(request, 'Sending otp error. Limit Exceeded. Please Contact Customer support' )
                                return render(request, 'accounts/validate_phone.html', context) 
                                #return Response({
                                #    'status' : False,
                                #    'detail' : 'Sending otp error. Limit Exceeded. Please Contact Customer support'
                                #})

                            old.count = count +1
                            old.save()
                            print('Count Increase', count)

                            conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=988e9a6f-9c72-11eb-80ea-0200cd936042&to="+phone+"&otpvalue="+str(key)+"&templatename=WomenMark1")
                            res = conn.getresponse() 
                            
                            data = res.read()
                            data=data.decode("utf-8")
                            data=ast.literal_eval(data)
                            print(data)
                            
                            if data["Status"] == 'Success':
                                old.otp_session_id = data["Details"]
                                old.otp = key
                                old.save()
                                print('In validate phone :'+old.otp_session_id)
                                messages.success(request, 'OTP sent successfully' )

                                
                                return render(request, 'accounts/validate_phone.html', context) 
                                #return render(request, 'accounts/validate_phone.html')
                                #return Response({
                                #        'status' : True,
                                #        'detail' : 'OTP sent successfully'
                                #    })    
                            else:
                                messages.error(request, 'OTP sending Failed' )
                                return render(request, 'accounts/validate_phone.html', context) 
                                #return Response({
                                #        'status' : False,
                                #        'detail' : 'OTP sending Failed'
                                #    }) 

                            


                        else:

                            obj=PhoneOTP.objects.create(
                                phone=phone,
                                otp = key,
                                #email=email,
                                username=username,
                                #password=password,
                            )
                            conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=988e9a6f-9c72-11eb-80ea-0200cd936042&to="+phone+"&otpvalue="+str(key)+"&templatename=WomenMark1")
                            res = conn.getresponse()    
                            data = res.read()
                            print(data.decode("utf-8"))
                            data=data.decode("utf-8")
                            data=ast.literal_eval(data)

                            if data["Status"] == 'Success':
                                obj.otp_session_id = data["Details"]
                                obj.save()
                                print('In validate phone :'+obj.otp_session_id)
                                messages.success(request, 'OTP sent successfully' )
                                return render(request, 'accounts/validate_phone.html', context) 
                                #return Response({
                                #        'status' : True,
                                #        'detail' : 'OTP sent successfully'
                                #    })    
                            else:
                                messages.error(request, 'OTP sending Failed' )
                                return render(request, 'accounts/validate_phone.html', context) 
                                #return Response({
                                #        'status' : False,
                                #        'detail' : 'OTP sending Failed'
                                #    })

                            
                    else:
                        messages.error(request, 'Sending OTP error' )
                        return render(request, 'accounts/validate_phone.html', context) 
                        #    return Response({
                        #        'status' : False,
                        #        'detail' : 'Sending otp error'
                        #    })   

        else:
            messages.error(request, 'Phone number is not given in post request' )
            return render(request, 'pages/index.html')
            #return Response({
            #    'status' : False,
            #    'detail' : 'Phone number is not given in post request'
            #}) 
    else:
        current_user = request.user.username
        if current_user.isdigit():
            user_data = Employee.objects.filter(uid=current_user)
            phone = user_data.first().phone
        else:
            user_data = Employer.objects.filter(firm_name=current_user)
            phone = user_data.first().phone
        context={
            'current_user': current_user,
            'phone' : phone
        }  
        return render(request, 'accounts/validate_phone.html', context)         



def send_otp(phone):
    if phone:
        key = random.randint(999,9999)
        print(key)
        return key
    else:
        return False



def ValidateOTP(request, *args, **kwargs):
    current_user = request.user.username
    if current_user.isdigit():
        user_data = Employee.objects.filter(uid=current_user)
        
    else:
        user_data = Employer.objects.filter(firm_name=current_user)
            
    if request.method == 'POST':
        phone = request.POST.get('phone', False)
        otp_sent = request.POST.get('otp_sent', False)
        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp_session_id = old.otp_session_id
                print("In validate otp"+otp_session_id)
                conn.request("GET", "https://2factor.in/API/V1/988e9a6f-9c72-11eb-80ea-0200cd936042/SMS/VERIFY/"+otp_session_id+"/"+otp_sent)
                res = conn.getresponse()    
                data = res.read()
                print(data.decode("utf-8"))
                data=data.decode("utf-8")
                data=ast.literal_eval(data)
                
                

                if data["Status"] == 'Success':
                    old.validated = True
                    user_data.first().phone_verified = True
                    old.save()
                    user_data.first().save()
                    messages.success(request, 'OTP MATCHED. Please proceed for registration.')
                    return redirect('subscription')
                    #return Response({
                    #    'status' : True,
                    #    'detail' : 'OTP MATCHED. Please proceed for registration.'
                    #        })

                else:
                    messages.error(request, 'OTP INCORRECT')
                    return redirect('validate_phone')
                    #return Response({
                    #    'status' : False,
                    #    'detail' : 'OTP INCORRECT'
                    #})
                


            else:
                messages.error(request, 'First Proceed via sending otp request')
                return redirect('validate_phone')
                #return Response({
                #       'status' : False,
                #        'detail' : 'First Proceed via sending otp request'
                #    })


        else:
            messages.error(request, 'Please provide both phone and otp for Validation')
            return redirect('validate_phone')
            #return Response({
            #            'status' : False,
            #            'detail' : 'Please provide both phone and otp for Validation'
            #        })
