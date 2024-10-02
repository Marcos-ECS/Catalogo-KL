from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signupKL'),
    path('login/', views.loginkl, name='loginuser'),
    path('logout/', views.logoutkl, name='logoutkl'),
]
