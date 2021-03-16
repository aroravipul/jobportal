from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register_ee', views.register_ee, name='register_ee'),
    path('register_er', views.register_er, name='register_er'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard')
]