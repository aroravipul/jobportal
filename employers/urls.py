from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='employers'),
    path('<int:employer_id>', views.employer, name='employer'),
    path('search', views.search, name='search'),
]