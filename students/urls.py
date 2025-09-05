from django.urls import path
from . import views

urlpatterns = [
    path('materials/', views.materials, name='students_materials'),
    path('export-books/', views.export_books_csv, name='export_books'),
    path('demos/', views.demos, name='demos'),
    path('demos/<slug:slug>/', views.demo_detail, name='demo_detail'),
]
