from django.contrib import admin
from .models import Employer, Job

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('firm_name', 'requirement', 'is_published', 'is_approved')
    list_filter = ('requirement',)
    list_editable = ('is_published','is_approved')
    search_fields = ('requirement',)
    list_per_page = 25

class JobAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'job_category')
    list_filter = ('job_category',)
    search_fields = ('job_name', 'job_category')
    list_per_page = 25

admin.site.register(Job, JobAdmin)
admin.site.register(Employer, EmployerAdmin)

