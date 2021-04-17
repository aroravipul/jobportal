from django.urls import path, include #, re_path
from . import views
#from .views import *
#app_name = 'accounts'

urlpatterns = [
    path('login', views.login, name='login'),
    path('register_ee', views.register_ee, name='register_ee'),
    path('register_er', views.register_er, name='register_er'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('profile/<str:name>', views.profile, name='profile'),
    path('profile_ee', views.profile_ee, name='profile_ee'),
    path('profile_er', views.profile_er, name='profile_er'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('generate_otp/<int:id>', views.generate_otp, name='generate_otp'),
    path('match_otp/<int:id>/<int:ad_id>', views.match_otp, name='match_otp'),
    path('subscription', views.subscription, name='subscription'),
    path('validate_phone', views.ValidatePhoneSendOTP, name='validate_phone'),
    path('validate_otp', views.ValidateOTP, name='validate_otp')
    #re_path('^validate_phone/', ValidatePhoneSendOTP.as_view(), name='validatephone'),
]