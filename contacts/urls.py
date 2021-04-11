from django.urls import path
from . import views

urlpatterns = [
    path('contact_employee', views.contact_employee, name='contact_employee'),
    path('contact_employer/<str:id>', views.contact_employer, name='contact_employer')
]