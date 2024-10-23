from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.db import IntegrityError
from django.contrib import messages
from .forms import ProyectoFormulario, RegistroFormulario, ImagenesdeProyectoFormSet
from .models import Proyecto, ImagenesdeProyecto 
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
         form_proyecto = ProyectoFormulario()
         formset_imagenes = ImagenesdeProyectoFormSet(queryset=ImagenesdeProyecto.objects.none())
         return render(request, 'create_project.html', {
             'form': ProyectoFormulario, 'formset_imagenes': formset_imagenes
     })
     else:
        try:
            form_proyecto = ProyectoFormulario(request.POST, request.FILES)
            formset_imagenes = ImagenesdeProyectoFormSet(request.POST, request.FILES)

            #Guardar nuevo proyecto
            if form_proyecto.is_valid() and formset_imagenes.is_valid():
                new_project = form_proyecto.save(commit=False)
                new_project.Empleado_Responsable = request.user
                new_project.save()

                # Guardar las imágenes del formset asociadas al nuevo proyecto
                for form in formset_imagenes:
                    imagen_proyecto = form.save(commit=False)
                    imagen_proyecto.proyecto = new_project  # Asignar el proyecto a la imagen
                    imagen_proyecto.save()

            return redirect ('task')
        except ValueError:
             return render(request, 'create_project.html', {
                'form': form_proyecto,
                'formset_imagenes': formset_imagenes,
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
             form = ProyectoFormulario(request.POST, request.FILES, instance=task)
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

def Detalles_proyecto(request, project_id):
    # Obtener el proyecto o lanzar un error 404 si no existe
    proyecto = get_object_or_404(Proyecto, pk=project_id)
    return render(request, 'task_pdetails.html', {'proyecto': proyecto})

def logoutkl(request):
     logout(request)
     messages.info(request, 'Has cerrado la sesion')
     return redirect('home')