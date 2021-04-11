from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.query_utils import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Employer, Ad, Job
from django.contrib import messages, auth
from contacts.models import Employee_to_employer
# Create your views here.

def index(request):
    employers = Ad.objects.filter(is_published=True)

    paginator = Paginator(employers, 3)
    page = request.GET.get('page')
    paged_employers = paginator.get_page(page)
    if request.user.username.isdigit():
        print('i am employee')
        logged_user = "employee"
    else:
        logged_user = "employer"

    context = {
        'employers': paged_employers,
        'shift_choices': Ad.SHIFT_OFFERED_CHOICES,
        'logged_user' : logged_user
    }
    return render(request, 'employers/index_employer.html', context)
    

def view_ad(request, id):
    
    if request.method == 'POST':
        get_ad = Ad.objects.get(id=id)
        
        firm_name = request.POST['firm']
        requirement = request.POST['requirement']
        no_of_requirments = request.POST['no_of_requirments'] 
        salary_offered = request.POST['salary_offered']
        salary_frequency = request.POST['salary_frequency']
        shift_offered = request.POST['shift_offered']
        firm = Employer.objects.get(firm_name=firm_name)
        requirement_id = Job.objects.get(job_name=requirement)

        get_ad.firm=firm
        get_ad.requirement=requirement_id
        get_ad.no_of_requirments=no_of_requirments
        get_ad.salary_offered=salary_offered
        get_ad.salary_frequency=salary_frequency
        get_ad.shift_offered=shift_offered
        get_ad.save()

        messages.success(request, 'Your ad is saved successfully.')
        return redirect('dashboard')

def employer(request, id):
    employer = get_object_or_404(Ad, pk=id)
    if request.user.username.isdigit():
        contacts_by_user = Employee_to_employer.objects.order_by('-contact_date').filter(employee_id=request.user.username).filter(ad_id_id=id)
        contacts_by_user_count = Employee_to_employer.objects.order_by('-contact_date').filter(employee_id=request.user.username).count()
    
        print(contacts_by_user_count)
        print(contacts_by_user)
        logged_user = "employee"
    else:
        logged_user = "employer"
    context = {
        'employer' : employer,
        'logged_user' : logged_user,
        'contacts_by_user': contacts_by_user,
        'contacts_by_user_count': contacts_by_user_count
    }
    return render(request, 'employers/employer.html', context)

def search(request):
    queryset_list = Ad.objects.order_by('-create_date').filter(is_published=True)
    #job preference 
    if 'jobpref' in request.GET:
        jobpref = request.GET['jobpref']
        if jobpref:
            queryset_list = queryset_list.filter(requirement__job_name__icontains=jobpref)

    # city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(firm__city__icontains=city)

    # salary
    if 'Salary' in request.GET:
        salary = request.GET['Salary']
        if salary:
            queryset_list = queryset_list.filter(salary_offered__lte=salary)

    # shifts
    if 'shift' in request.GET:
        shift = request.GET['shift']
        if shift:
            queryset_list = queryset_list.filter(shift_offered__iexact=shift)
    
    # previous experience
    if 'prevexp' in request.GET:
        prevexp = request.GET['prevexp']
        if prevexp:
            queryset_list = queryset_list.filter(requirement__job_name__icontains=prevexp)

    context = {
        'shift_choices': Ad.SHIFT_OFFERED_CHOICES,
        'employers': queryset_list,
        'values' : request.GET
    }
    return render(request, 'employers/search.html', context)

def post_ad(request):
    #print("m here")
    employer_id = Employer.objects.values_list('id', flat=True).filter(firm_name=request.user.username)
    ads_by_user = Ad.objects.filter(firm=employer_id.first()).count()
    print(ads_by_user)
    if ads_by_user >= 3:
        messages.error(request, 'Your ad cannot be posted as you have reached the maximum limit(3) of posting ads.')
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            print("No, m here")
            firm_name = request.POST['firm']
            requirement = request.POST['requirement']
            no_of_requirments = request.POST['no_of_requirments'] 
            salary_offered = request.POST['salary_offered']
            salary_frequency = request.POST['salary_frequency']
            shift_offered = request.POST['shift_offered']
            firm = Employer.objects.get(firm_name=firm_name)
            requirement_id = Job.objects.get(job_name=requirement)

            # check if number of ads by this employer is 3.
            #employer_ads = Ad.objects.get(firm=firm)
            #print(employer_ads)
            new_ad = Ad(firm=firm, requirement=requirement_id, no_of_requirments=no_of_requirments,
                salary_offered=salary_offered, salary_frequency=salary_frequency, shift_offered=shift_offered)
            new_ad.save()

            messages.success(request, 'Your ad is submitted successfully. Our team will review and approve it soon.')
            return redirect('dashboard')

        else:
            job_list = Job.objects.all()
            print(job_list)
            context = {
                'jobs': job_list,
                'salary_choices': Ad.SALARY_CHOICES,
                'shift_choices': Ad.SHIFT_OFFERED_CHOICES,
            }
            return render(request, 'employers/post_ad.html', context)
        
        
def del_ad(request, id):
    Ad.objects.filter(id=id).delete()
    messages.success(request, 'Ad deleted successfully')
    return redirect('dashboard')

    