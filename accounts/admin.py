from django.contrib import admin
from .models import User_category, Subscription_employee, Subscription_employer

class User_categoryAdmin(admin.ModelAdmin):
    list_display = ('username',)

class Subscription_employeeAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'is_active', 'price')

class Subscription_employerAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'is_active', 'price')


admin.site.register(User_category, User_categoryAdmin)
admin.site.register(Subscription_employee, Subscription_employeeAdmin)
admin.site.register(Subscription_employer, Subscription_employerAdmin)