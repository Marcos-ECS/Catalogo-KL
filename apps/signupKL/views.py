from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.db import IntegrityError
from django.contrib import messages
from .forms import ProyectoFormulario, RegistroFormulario
from .models import Proyecto 
from django.contrib.auth.decorators import login_required
# Create your views here.
#Registro de usuaurios
@login_required
def signup(request):
    if request.method == 'GET':
        return render (request, 'signkl.html',{
        'form': RegistroFormulario
        
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
                    'form': RegistroFormulario,
                    "error": 'El usuario ya existe'
                })
        return render(request, 'signkl.html',{
            'form': RegistroFormulario,
            "error": 'La contraseña no coincide'
        })
    
@login_required    
def task(request):
     task = Proyecto.objects.all().order_by('-FechaDeAgregado')
     return render(request, 'task.html', {'task': task})

@login_required
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

@login_required        
def Editar_proyectos(request, project_id):
     if request.method == 'GET':
        task = get_object_or_404(Proyecto, pk=project_id)
        form = ProyectoFormulario(instance=task)
        return render(request, 'project_edit.html', {'task':task, 'form': form})
     else:
         try:
             task = get_object_or_404(Proyecto, pk=project_id)
             form = ProyectoFormulario(request.POST, instance=task)
             form.save()
             return redirect('task')
         except ValueError:
             return render(request, 'project_edit.html',{'task':task, 'form':form, 'error': "Error al actualizar proyecto"})

def Proyectos_publicado(request):
    task = Proyecto.objects.filter(Estatus_de_proyecto = 'Si').order_by('-FechaDeAgregado')
    return render(request, 'task_publicados.html', {'task': task})

# def Borrar_proyecto(request, project_id):
#     task = get_object_or_404(Proyecto, pk=project_id)
#     if request.method == 'POST':
#         task.delete()
#         return redirect('task')

def logoutkl(request):
     logout(request)
     messages.info(request, 'Has cerrado la sesion')
     return redirect('home')