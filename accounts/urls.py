from django.urls import path
from . import views

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
    path('subscription', views.subscription, name='subscription')
]