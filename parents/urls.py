from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='parents_about'),
    path('individual/', views.individual, name='parents_individual'),
    path('groups/', views.groups, name='parents_groups'),
    path('selfstudy/', views.selfstudy, name='parents_selfstudy'),
]
