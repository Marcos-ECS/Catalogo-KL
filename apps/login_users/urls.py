from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='login'),
    # Otras rutas de la aplicación 'users'
]
