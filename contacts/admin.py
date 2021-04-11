from django.contrib import admin
from .models import Employer_to_employee, Employee_to_employer

class ContactEmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'firm_name', 'employee_phone', 'contact_date')
    list_display_links = ('employee_id', 'firm_name')
    search_fields = ('employee_id', 'firm_name')
    list_per_page = 25

class ContactEmployerAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'ad_id', 'employer_phone', 'contact_date')
    list_display_links = ('employee_id', 'ad_id')
    search_fields = ('employee_id', 'ad_id')
    list_per_page = 25

admin.site.register(Employer_to_employee, ContactEmployeeAdmin)
admin.site.register(Employee_to_employer, ContactEmployerAdmin)