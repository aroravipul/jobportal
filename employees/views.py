from django.shortcuts import render, get_object_or_404
from django.db.models.query_utils import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Employee



def index(request):
    employees = Employee.objects.order_by('-create_date').filter(is_published=True).filter(is_approved=True)

    paginator = Paginator(employees, 3)
    page = request.GET.get('page')
    paged_employees = paginator.get_page(page)

    context = {
        'employees': paged_employees,
        'shift_choices': Employee.SHIFT_OFFERED_CHOICES
    }
    return render(request, 'employees/index_employee.html', context)

def employee(request, employee_uid):
    employee = get_object_or_404(Employee, pk=employee_uid)

    context = {
        'employee' : employee
    }
    return render(request, 'employees/employee.html', context)

def search(request):
    queryset_list = Employee.objects.order_by('-create_date').filter(is_published=True).filter(is_approved=True)

    #job preference 
    if 'jobpref' in request.GET:
        jobpref = request.GET['jobpref']
        if jobpref:
            queryset_list = queryset_list.filter(Q(job_preference1__job_name__icontains=jobpref) | Q(job_preference1__job_name__icontains=jobpref) | Q(job_preference1__job_name__icontains=jobpref))

    # city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__icontains=city)

    # salary
    if 'Salary' in request.GET:
        salary = request.GET['Salary']
        if salary:
            queryset_list = queryset_list.filter(exp_salary__lte=salary)

    # shifts
    if 'shift' in request.GET:
        shift = request.GET['shift']
        if shift:
            queryset_list = queryset_list.filter(pref_shift__iexact=shift)
    
    # previous experience
    if 'prevexp' in request.GET:
        prevexp = request.GET['prevexp']
        if prevexp:
            queryset_list = queryset_list.filter(prev_work_exp__icontains=prevexp)

    context = {
        'shift_choices': Employee.SHIFT_OFFERED_CHOICES,
        'employees': queryset_list,
        'values' : request.GET
    }
    return render(request, 'employees/search.html', context)
