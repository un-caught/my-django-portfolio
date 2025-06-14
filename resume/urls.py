from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('service/', views.services, name="services"),
    path('projects/', views.projects, name="projects"),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('resume/', views.resume, name='resume'),
    path('contact/', views.contact, name='contact'),

]