from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginkl, name='loginkl'),
    # Otras rutas de la aplicación 'users'
]
