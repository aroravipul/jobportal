from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'employers/index_employer.html')

def employer(request):
    return render(request, 'employers/employer.html')

def search(request):
    return render(request, 'employers/search.html')
from django.shortcuts import render

# Create your views here.
