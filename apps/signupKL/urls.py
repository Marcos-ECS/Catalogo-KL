from django.urls import path
from django.conf.urls.static import static
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('', views.signup, name='signup'),
    path('task/', views.task, name='task'),
    path('task/create', views.crear_proyectos, name='create_project'),
    path('task_published', views.Proyectos_publicado, name='published_projects'),
    path('task/<int:project_id>', views.Editar_proyectos, name='project_edit'),
    path('task/<int:project_id>/', views.Detalles_proyecto, name='detail_project'),
    path('proyecto/<int:project_id>/descargar/', views.descargar_proyecto_pdf, name='descargar_proyecto_pdf'),
    path('proyecto/<int:project_id>/editar/', views.Editar_proyectos, name='project_edit'),
    path('proyecto/<int:project_id>/ver/', views.Editar_proyecto_NO_autor, name='Editar_proyecto_NO_autor'),
    path('descargar_csv/', views.descargar_csv, name='descargar_csv'),
    #path('task/<int:project_id>/delete', views.Borrar_proyecto, name='delete_project'),
    path('logout/', views.logoutkl, name='logoutkl'),
    path('perfil/', views.perfil, name='perfil'),
    path('error-permisos/', views.error_permisos, name='error_permisos'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin/listar-usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('admin/usuarios/<int:usuario_id>/', views.detalle_usuario, name='detalle_usuario'),
    path('buscar_usuarios/', views.buscar_usuarios, name='buscar_usuarios'),
    path('proyecto/<int:project_id>/descargar/visitantes/', views.descargar_proyecto_pdf_visitantes, name='descargar_proyecto_pdf_visitantes'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])