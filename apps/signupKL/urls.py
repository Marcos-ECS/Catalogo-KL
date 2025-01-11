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
    path('task/auth/<int:project_id>/', views.Detalles_proyecto_autenticado, name='detail_project_autenticado'),
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
    path('task_published_autenticados', views.Proyectos_publicado_autenticados, name='published_projects_autenticados'),
    path('admin/listar-usuarios-sin-admins/', views.listar_usuarios_sin_admins, name='listar_usuarios_sin_admins'),
    path('admin/bloquear-usuario/<int:usuario_id>/', views.bloquear_usuario, name='bloquear_usuario'),
    path('admin/desbloquear-usuario/<int:usuario_id>/', views.desbloquear_usuario, name='desbloquear_usuario'),
    path('admin/exportar-logs-sesion/', views.exportar_logs_inicio_sesion, name='exportar_logs_sesion'),
    path('admin/exportar-logs-proyectos/', views.exportar_logs_proyectos, name='exportar_logs_proyectos'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])