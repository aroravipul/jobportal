from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee_to_employer, Employer_to_employee
from employers.models import Employer, Ad

# Create your views here.

def contact_employee(request):
    if request.method ==  'POST':
        ad = request.POST.get('ad')
        employee_id = request.POST.get('employee_id', False)
        firm_name = request.POST.get('firm_name', False)
        fullname = request.POST.get('fullname', False)
        #phone = request.POST.get('phone', False)

        # Check if user has already shown interest in a profile
        ad_id = Ad.objects.get(id=ad)
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Employer_to_employee.objects.all().filter(employee_id=employee_id, employer_ad=ad_id)
            if has_contacted:
                messages.error(request, 'You have already shown interest in this profile')
                return redirect('/employees/'+employee_id)
                
        contact_ee = Employer_to_employee(employer_ad=ad_id, employee_id=employee_id, firm_name=firm_name)
        contact_ee.save()
        
        messages.success(request, 'Your profile interest is submitted successfully')
        return redirect('/employees/'+employee_id)
    else:
        
        return render(request, '/employees/'+employee_id)
   


def contact_employer(request, id):
    if request.method ==  'POST':
        print("I am here")
        requirement = request.POST.get('requirement')
        print(requirement)
        uid = request.POST.get('uid', False)
        fullname = request.POST.get('fullname', False)
        #phone = request.POST.get('phone', False)
        contacted_ad = Ad.objects.get(id=id)
        print(contacted_ad)

        if request.user.is_authenticated:
            #user_id = request.user.id
            #print(user_id)
            has_contacted = Employee_to_employer.objects.all().filter(employee_id=uid, ad_id=contacted_ad)
            #page_id = Ad.objects.filter(firm_name=firm_name)
            #print(page_id)
            if has_contacted:
                messages.error(request, 'You have already shown interest in this profile')
                return redirect('/employers/'+id)

        contact_er = Employee_to_employer(employee_id=uid, ad_id=contacted_ad, employee_fullname=fullname)
        contact_er.save()
        
        
        messages.success(request, 'Your profile interest is submitted successfully')
        
        return redirect('/employers/'+id)
        
