from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='employers'),
    path('<int:id>', views.employer, name='employer'),
    path('search', views.search, name='ersearch'),
    path('post_ad', views.post_ad, name='post_ad'),
    path('view_ad/<int:id>', views.view_ad, name='view_ad'),
    path('del_ad/<int:id>', views.del_ad, name='del_ad')
]