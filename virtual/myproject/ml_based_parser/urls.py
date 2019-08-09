from django.urls import path

from . import views

urlpatterns = [
    path('health_check/', views.health_check, name='health_check'),
    path('parse_resume_file/', views.parse_resume_file, name='parse_resume_file'),
    path('candidates_parsed_resume/', views.get_candidate_parsed_resume, name='candidates_parsed_resume'),
]
