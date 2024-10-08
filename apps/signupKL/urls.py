from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signupKL'),
    path('task/', views.task, name='task'),
    path('task/create', views.crear_proyectos, name='create_project'),
    path('task/<int:project_id>', views.Editar_proyectos, name='project_edit'),
    path('logout/', views.logoutkl, name='logoutkl'),
]
