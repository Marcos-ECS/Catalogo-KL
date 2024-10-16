from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signupKL'),
    path('task/', views.task, name='task'),
    path('task/create', views.crear_proyectos, name='create_project'),
    path('task_published', views.Proyectos_publicado, name='published_projects'),
    path('task/<int:project_id>', views.Editar_proyectos, name='project_edit'),
    path('task/<int:project_id>/delete', views.Borrar_proyecto, name='delete_project'),
    path('logout/', views.logoutkl, name='logoutkl'),
]
