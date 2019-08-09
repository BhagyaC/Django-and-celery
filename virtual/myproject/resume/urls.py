from django.urls import path

from . import views

urlpatterns = [
    path('parse/', views.async_parser, name='parser'),
    
]
