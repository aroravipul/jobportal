from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages, auth
from employees.models import Employee
from employees.forms import EmployeeForm
from employers.models import Employer, Job, Ad
from volunteers.models import Volunteer
from .models import User_category, Subscription_employee, Subscription_employer
from employers.forms import EmployerForm
from django.contrib.auth.models import User
from contacts.models import Employee_to_employer, Employer_to_employee
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','jobportal.settings')
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import django
django.setup()

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
        context = {
            'is_employee': is_employee,
            'contacts_for_u': contacts_for_u,
            'contacts_by_u': contacts_by_u
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

                messages.success(request, 'Your profile is updated successfully')
                return HttpResponseRedirect('subscription')
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

            messages.success(request, 'Your profile is updated successfully')
            return HttpResponseRedirect('subscription')
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


