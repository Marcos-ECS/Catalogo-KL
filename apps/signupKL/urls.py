from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signupKL'),
    path('task/', views.task, name='task'),
    path('task/create', views.crear_proyectos, name='create_project'),
    path('logout/', views.logoutkl, name='logoutkl'),
]
