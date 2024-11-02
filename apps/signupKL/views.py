from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.db import IntegrityError
from django.contrib import messages
from .forms import ProyectoFormulario, RegistroFormulario, ImagenesdeProyectoFormSetCrear, ImagenesdeProyectoFormSetEditar, ImagenesdeProyectoFormSetSoloLectura
from .models import Proyecto, ImagenesdeProyecto 
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import csv

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
         formset_imagenes = ImagenesdeProyectoFormSetCrear(queryset=ImagenesdeProyecto.objects.none())
         return render(request, 'create_project.html', {
             'form': ProyectoFormulario, 'formset_imagenes': formset_imagenes
     })
     else:
        try:
            form_proyecto = ProyectoFormulario(request.POST, request.FILES)
            formset_imagenes = ImagenesdeProyectoFormSetCrear(request.POST, request.FILES)

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
    task = get_object_or_404(Proyecto, pk=project_id)
    
    if task.Empleado_Responsable != request.user:
        return redirect('Editar_proyecto_NO_autor', project_id=task.id)

    if request.method == 'GET':
        form = ProyectoFormulario(instance=task)
        formset_imagenes = ImagenesdeProyectoFormSetEditar(queryset=ImagenesdeProyecto.objects.filter(proyecto=task))  # Cargar imágenes actuales
        return render(request, 'project_edit.html', {'task': task, 'form': form, 'formset_imagenes': formset_imagenes, 'es_creador': True})
    
    else:
        try:
            # Procesar el formulario del proyecto
            form = ProyectoFormulario(request.POST, request.FILES, instance=task)
            formset_imagenes = ImagenesdeProyectoFormSetEditar(request.POST, request.FILES, queryset=ImagenesdeProyecto.objects.filter(proyecto=task))
            
            if form.is_valid() and formset_imagenes.is_valid():
                # Guardar cambios en el proyecto (incluyendo el estatus)
                form.save()

                # Procesar las imágenes en el formset
                for form in formset_imagenes:
                    imagen_proyecto = form.save(commit=False)

                    # Verificar si la imagen está marcada para eliminar
                    if form.cleaned_data.get('DELETE'):
                        if imagen_proyecto.pk:  # Si existe en la BD, eliminarla
                            imagen_proyecto.delete()
                    # Guardar solo si hay una imagen nueva
                    elif form.cleaned_data.get('imagen'):
                        imagen_proyecto.proyecto = task  # Asignar el proyecto a la imagen
                        imagen_proyecto.save()

                # Guardar los cambios en el formset (posible duplicidad de datos? invenstigar y testear)
                #formset_imagenes.save()

                return redirect('task')

            else:
                # Mostrar los errores del formulario y del formset
                return render(request, 'project_edit.html', {
                    'task': task,
                    'form': form,
                    'formset_imagenes': formset_imagenes,
                    'error': "Error al actualizar el proyecto",
                    'form_errors': form.errors,
                    'formset_errors': formset_imagenes.errors,
                })

        except ValueError:
            return render(request, 'project_edit.html', {
                'task': task,
                'form': form,
                'formset_imagenes': formset_imagenes,
                'error': "Error al actualizar proyecto"
            })


def Proyectos_publicado(request):
    task = Proyecto.objects.filter(Estatus_de_proyecto = 'Si').order_by('-FechaDeAgregado')
    return render(request, 'task_publicados.html', {'task': task})

@login_required
def Editar_proyecto_NO_autor(request, project_id):
    # Obtener el proyecto y verificar que exista
    task = get_object_or_404(Proyecto, pk=project_id)
    form = ProyectoFormulario(instance=task)
    formset_imagenes = ImagenesdeProyectoFormSetSoloLectura(queryset=ImagenesdeProyecto.objects.filter(proyecto=task))

    # Deshabilitar todos los campos del formulario y del formset
    for field in form.fields.values():
        field.disabled = True
    for form in formset_imagenes:
        for field in form.fields.values():
            field.disabled = True

    # Renderizar el template de edición en modo de solo lectura
    return render(request, 'project_edit.html', {
        'task': task,
        'form': form,
        'formset_imagenes': formset_imagenes,
        'es_creador': False,  # Pasar al template que no es el creador
        'descripcion': task.descripcion,
        'fecha_de_agregado': task.FechaDeAgregado,
        'fecha_de_realizacion': task.Fecha_De_Realizacion,
    })


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

#Exportador de PDF
@login_required
def descargar_proyecto_pdf(request, project_id):
    proyecto = get_object_or_404(Proyecto, pk=project_id)

    # Configurar la respuesta como archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{proyecto.titulo}.pdf"'

    # Crear el PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Título del proyecto
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 100, f"Proyecto: {proyecto.titulo}")

    # Descripción
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 140, f"Descripción: {proyecto.descripcion}")

    # Fecha de agregado y realización
    p.drawString(100, height - 160, f"Fecha de agregado: {proyecto.FechaDeAgregado}")
    if proyecto.Fecha_De_Realizacion:
        p.drawString(100, height - 180, f"Fecha de realización: {proyecto.Fecha_De_Realizacion}")

    # Empleado Responsable
    p.drawString(100, height - 200, f"Empleado responsable: {proyecto.Empleado_Responsable}")

    # Imágenes de la galería
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 240, "Imágenes de la galería:")
    imagenes = ImagenesdeProyecto.objects.filter(proyecto=proyecto)
    y_position = height - 260
    for imagen in imagenes:
        if imagen.imagen:  # Verifica si hay un archivo de imagen asociado
            p.drawString(120, y_position, f"- {imagen.imagen.url}")  # Solo URL por simplicidad
        else:
            p.drawString(120, y_position, "- Imagen de muestra")
        y_position -= 20

    # Finalizar el PDF
    p.showPage()
    p.save()
    return response

#Exportador de CSV
@login_required
def descargar_csv(request):
    # Crear la respuesta de CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="proyectos.csv"'

    # Definir los encabezados del CSV
    writer = csv.writer(response)
    writer.writerow(['ID', 'Título', 'Descripción', 'Fecha de subida', 'Estatus', 'Autor'])

    # Obtener los proyectos y escribir cada uno en el CSV
    proyectos = Proyecto.objects.all()
    for proyecto in proyectos:
        writer.writerow([
            proyecto.id,
            proyecto.titulo,
            proyecto.descripcion,
            proyecto.FechaDeAgregado,
            #proyecto.Fecha_De_Realizacion,
            proyecto.get_Estatus_de_proyecto_display(),
            proyecto.Empleado_Responsable.username
        ])gi

    return response