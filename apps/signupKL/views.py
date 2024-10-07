from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.db import IntegrityError
from django.contrib import messages
from .forms import ProyectoFormulario

# Create your views here.
#Registro de usuaurios
def signup(request):
    if request.method == 'GET':
        return render (request, 'signkl.html',{
        'form': UserCreationForm
        
    })
    else:
        if request.POST ['password1'] == request.POST['password2']:
            try:
                #registro
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                #login(request, user)
                return redirect('task')   
            except IntegrityError:
                    return render (request, 'signkl.html',{
                    'form': UserCreationForm,
                    "error": 'El usuario ya existe'
                })
        return render(request, 'signkl.html',{
            'form': UserCreationForm,
            "error": 'La contraseña no coincide'
        })
    
def task(request):
     return render(request, 'task.html')

def crear_proyectos(request):
     if request.method == 'GET':
         return render(request, 'create_project.html', {
             'form': ProyectoFormulario
     })
     else:
        try:
            form = ProyectoFormulario(request.POST)
            new_project = form.save(commit=False)
            new_project.Empleado_Responsable = request.user
            new_project.save()
            return redirect ('task')
        except ValueError:
             return render(request, 'create_project.html', {
                'form': ProyectoFormulario,
                'error': 'Por favor proporcione datos validos'
        })

def logoutkl(request):
     logout(request)
     messages.info(request, 'Has cerrado la sesion')
     return redirect('/home/')