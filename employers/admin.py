from django.contrib import admin
from .models import Employer, Job, Ad

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('firm_name', 'is_published', 'is_approved', 'phone')
    list_filter = ('firm_name',)
    list_editable = ('is_published','is_approved')
    search_fields = ('firm_name',)
    list_per_page = 25

class JobAdmin(admin.ModelAdmin):
    list_display = ('job_name', 'job_category')
    list_filter = ('job_category',)
    search_fields = ('job_name', 'job_category')
    list_per_page = 25

class AdAdmin(admin.ModelAdmin):
    list_display = ('firm', 'requirement')
    list_filter = ('requirement',)
    #list_editable = ('is_published','is_approved')
    search_fields = ('firm',)
    list_per_page = 25

admin.site.register(Job, JobAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(Ad, AdAdmin)

