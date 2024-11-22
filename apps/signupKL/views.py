from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.db import IntegrityError
from django.contrib import messages
from .forms import ProyectoFormulario, RegistroFormulario, ImagenesdeProyectoFormSetCrear, ImagenesdeProyectoFormSetEditar, ImagenesdeProyectoFormSetSoloLectura, UserProfileForm
from .models import Proyecto, ImagenesdeProyecto 
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import csv
from .filters import ProyectoFilter
from django.contrib.auth.forms import UserChangeForm
from .forms import PerfilUsuarioForm
from .decorators import check_profile_completion
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from textwrap import wrap

# Create your views here.
#Registro de usuaurios
@check_profile_completion
@login_required
def signup(request):
    if request.method == 'POST':
        form = RegistroFormulario(request.POST)
        if form.is_valid():
            # Crear usuario
            form.save()
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('task')  # Redirigir a la página deseada
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = RegistroFormulario()
    
    return render(request, 'signkl.html', {'form': form, 'container': True})

@check_profile_completion
@login_required(login_url='loginkl')    
def task(request):
    proyectos = Proyecto.objects.all().order_by('-FechaDeAgregado')
    task = ProyectoFilter(request.GET, queryset=proyectos)
    return render(request, 'task.html', {'task': task, 'container': True})

@check_profile_completion
@login_required(login_url='loginkl')  
def crear_proyectos(request):
     if request.method == 'GET':
         form_proyecto = ProyectoFormulario()
         formset_imagenes = ImagenesdeProyectoFormSetCrear(queryset=ImagenesdeProyecto.objects.none())
         return render(request, 'create_project.html', {
             'form': ProyectoFormulario, 'formset_imagenes': formset_imagenes,'container': True 
     })
     else:
       
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
            else:
                # Enviar mensaje de error si la descripción es demasiado corta o hay otros errores
                if form_proyecto.errors.get('descripcion'):
                    messages.error(request, "La descripción debe tener al menos 50 caracteres.")
                    
                return render(request, 'create_project.html', {
                    'form': form_proyecto,
                    'formset_imagenes': formset_imagenes,
                    'error': 'Por favor proporcione datos válidos', 
                    'container': True 
                })

@check_profile_completion
@login_required(login_url='loginkl')          
def Editar_proyectos(request, project_id):
    task = get_object_or_404(Proyecto, pk=project_id)
    
    if task.Empleado_Responsable != request.user:
        return redirect('Editar_proyecto_NO_autor', project_id=task.id)

    if request.method == 'GET':
        form = ProyectoFormulario(instance=task)
        formset_imagenes = ImagenesdeProyectoFormSetEditar(queryset=ImagenesdeProyecto.objects.filter(proyecto=task))  # Cargar imágenes actuales
        return render(request, 'project_edit.html', {'task': task, 'form': form, 'formset_imagenes': formset_imagenes, 'es_creador': True, 'container': True })
    
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
    return render(request, 'task_publicados.html', {'task': task, 'container': True })

@check_profile_completion
@login_required(login_url='loginkl')  
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
        'fecha_de_realizacion': task.Fecha_De_Realizacion, 'container': True, 
    })


# def Borrar_proyecto(request, project_id):
#     task = get_object_or_404(Proyecto, pk=project_id)
#     if request.method == 'POST':
#         task.delete()
#         return redirect('task')


def Detalles_proyecto(request, project_id):
    # Obtener el proyecto o lanzar un error 404 si no existe
    proyecto = get_object_or_404(Proyecto, pk=project_id)
    return render(request, 'task_pdetails.html', {'proyecto': proyecto, 'container': True})

@login_required(login_url='loginkl')  
def logoutkl(request):
     logout(request)
     messages.info(request, 'Has cerrado la sesion')
     return redirect('home')

# Exportador de PDF con cabecera y pie de página
@login_required(login_url='loginkl')  
def descargar_proyecto_pdf(request, project_id):
    proyecto = get_object_or_404(Proyecto, pk=project_id)

    # Configurar la respuesta como archivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{proyecto.titulo}.pdf"'

    # Crear el PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    def draw_header_footer():
        # Cabecera
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(colors.darkblue)
        p.drawString(50, height - 50, "Klugelab - Reporte de Proyecto")
        p.line(50, height - 55, width - 50, height - 55)

        # Pie de página
        p.setFont("Helvetica", 10)
        p.setFillColor(colors.gray)
        p.drawString(50, 30, "Generado por Klugelab")
        p.drawString(width - 100, 30, f"Pág. {p.getPageNumber()}")
        p.line(50, 40, width - 50, 40)

    def add_watermark():
        # Marca de agua
        p.saveState()
        p.setFont("Helvetica-Bold", 60)
        p.setFillColor(colors.lightgrey)
        p.translate(width / 2, height / 2)
        p.rotate(45)  # Rotar el texto
        p.drawCentredString(0, 0, "KLUGE LAB")
        p.restoreState()

    # Dibujar cabecera, pie de página y marca de agua
    add_watermark()
    draw_header_footer()

    # Contenido principal
    y_position = height - 100
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.black)

    # Título del proyecto
    p.drawString(50, y_position, f"Proyecto: {proyecto.titulo}")
    y_position -= 30

    # Descripción con salto de línea automático
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, "Descripción:")
    y_position -= 20
    p.setFont("Helvetica", 12)
    description = proyecto.descripcion
    wrapped_text = wrap(description, 80)  # Ajusta el ancho de línea
    for line in wrapped_text:
        if y_position < 100:
            p.showPage()
            add_watermark()
            draw_header_footer()
            y_position = height - 100
        p.drawString(50, y_position, line)
        y_position -= 15

    # Espaciado extra antes de las imágenes
    y_position -= 30
    if y_position < 200:
        p.showPage()
        add_watermark()
        draw_header_footer()
        y_position = height - 100

    # Imágenes de la galería
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y_position, "Imágenes de la galería:")
    y_position -= 30

    imagenes = ImagenesdeProyecto.objects.filter(proyecto=proyecto)
    col_position = 50
    for idx, imagen in enumerate(imagenes):
        if y_position < 150:  # Salto de página si la imagen no cabe
            p.showPage()
            add_watermark()
            draw_header_footer()
            y_position = height - 100
            col_position = 50

        if imagen.imagen:
            img_path = ImageReader(imagen.imagen.path)
            p.drawImage(img_path, col_position, y_position - 100, width=200, height=100, preserveAspectRatio=True, mask='auto')
        else:
            p.setFont("Helvetica", 12)
            p.drawString(col_position, y_position, "Imagen de muestra no disponible")
        
        col_position += 220  # Espacio entre columnas
        if (idx + 1) % 2 == 0:  # Nueva fila cada dos imágenes
            col_position = 50
            y_position -= 120

    # Finalizar el PDF
    p.showPage()
    p.save()
    return response



#Exportador de CSV
@login_required(login_url='loginkl')  
def descargar_csv(request):
    # Obtener el filtro de la consulta
    filtro = request.GET.get('filtro', 'all')

    # Crear la respuesta de CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="proyectos_{filtro}.csv"'

    # Definir los encabezados del CSV
    writer = csv.writer(response)
    writer.writerow(['ID', 'Título', 'Descripción', 'Fecha de subida', 'Estatus', 'Autor'])

    # Filtrar los proyectos según el parámetro
    if filtro == 'activos':
        proyectos = Proyecto.objects.filter(Estatus_de_proyecto='Si')
    elif filtro == 'inactivos':
        proyectos = Proyecto.objects.filter(Estatus_de_proyecto='No')
    else:  # Por defecto, todos los proyectos
        proyectos = Proyecto.objects.all()

    # Escribir los proyectos en el CSV
    for proyecto in proyectos:
        writer.writerow([
            proyecto.id,
            proyecto.titulo,
            proyecto.descripcion,
            proyecto.FechaDeAgregado.strftime('%d/%m/%Y'), 
            proyecto.get_Estatus_de_proyecto_display(),
            proyecto.Empleado_Responsable.username
        ])

    return response


#Perfil de usuario registrado

@check_profile_completion
@login_required(login_url='loginkl')  
def perfil(request):
    return render(request, 'profile.html', {'usuario': request.user, 'container': True})

#Editar perfil

@check_profile_completion
@login_required(login_url='loginkl')  
def editar_perfil(request):
    user_profile = request.user.profile  # Relación OneToOne entre User y UserProfile
    if request.method == 'POST':
        # Manejar ambos formularios: datos del usuario y foto de perfil
        user_form = PerfilUsuarioForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
    else:
        user_form = PerfilUsuarioForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'editar_perfil.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'container': True
    })



