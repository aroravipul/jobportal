from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

def index_employer(request):
    return render(request, 'employers/index_employer.html')

def index_employee(request):
    return render(request, 'employees/index_employee.html')