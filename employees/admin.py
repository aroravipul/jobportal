from django.contrib import admin
from .models import Employee#, Qualification

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'uid', 'is_published','volunteer', 'create_date', 'is_approved')
    list_filter = ('volunteer',)
    list_editable = ('is_published','is_approved')
    search_fields = ('skills', 'prev_work_exp', 'job_preference1', 'job_preference2', 'job_preference3')
    list_per_page = 25


admin.site.register(Employee, EmployeeAdmin)
#admin.site.register(City)
#admin.site.register(Qualification)
