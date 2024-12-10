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
from django.utils.timezone import localtime
from apps.signupKL.models import EstatusDeProyecto
from .decorators import usuario_tipo_permitido, verificar_usuario_bloqueado
from django.db.models import Q



# Create your views here.
#Registro de usuaurios
@check_profile_completion
@login_required(login_url='loginkl')
@usuario_tipo_permitido(tipos_permitidos=['Admin'])
def signup(request):
    if request.method == 'POST':
        form = RegistroFormulario(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('admin_panel')
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = RegistroFormulario()

    return render(request, 'signkl.html', {'form': form, 'container': True})

@check_profile_completion
@login_required(login_url='loginkl')
@usuario_tipo_permitido(tipos_permitidos=['Admin', 'Empleado'])
def task(request):
    proyectos = Proyecto.objects.all().order_by('-FechaDeAgregado')
    task = ProyectoFilter(request.GET, queryset=proyectos)
    estatus_disponibles = EstatusDeProyecto.objects.all()  # Obtener todos los estatus disponibles
    return render(request, 'task.html', {
        'task': task,
        'estatus_disponibles': estatus_disponibles,
        'container': True
    })


@check_profile_completion
@login_required(login_url='loginkl')
@usuario_tipo_permitido(tipos_permitidos=['Admin', 'Empleado'])
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
                estatus_default = EstatusDeProyecto.objects.get(nombre='Propuesto')  # Estatus inicial
                new_project.estatus = estatus_default
                new_project.Empleado_Responsable = request.user
                new_project.save()


                # Guardar las imágenes del formset asociadas al nuevo proyecto
                for form in formset_imagenes:
                    imagen_proyecto = form.save(commit=False)
                    imagen_proyecto.proyecto = new_project  # Asignar el proyecto a la imagen
                    imagen_proyecto.save()

                return redirect ('task')
            else:
                # Capturar errores específicos
                errores = {}
                if 'descripcion' in form_proyecto.errors:
                    errores['descripcion'] = form_proyecto.errors['descripcion']
                if not formset_imagenes.is_valid():
                    errores['galeria'] = "Hay errores en las imágenes de la galería. Por favor revisa los campos."

                return render(request, 'create_project.html', {
                    'form': form_proyecto,
                    'formset_imagenes': formset_imagenes,
                    'errores': errores,  # Pasar errores específicos al template
                    'container': True 
                })

@check_profile_completion
@login_required(login_url='loginkl')
@usuario_tipo_permitido(tipos_permitidos=['Admin', 'Empleado'])
def Editar_proyectos(request, project_id):
    task = get_object_or_404(Proyecto, pk=project_id)
    
    if task.Empleado_Responsable != request.user:
        return redirect('Editar_proyecto_NO_autor', project_id=task.id)

    if request.method == 'GET':
        form = ProyectoFormulario(instance=task)
        formset_imagenes = ImagenesdeProyectoFormSetEditar(queryset=ImagenesdeProyecto.objects.filter(proyecto=task))  # Cargar imágenes actuales
        estatus_actual = task.estatus.id if task.estatus else None
        estatus_disponibles = EstatusDeProyecto.objects.all()
        return render(request, 'project_edit.html', {
            'task': task,
            'form': form,
            'formset_imagenes': formset_imagenes,
            'estatus_actual': estatus_actual,
            'estatus_disponibles': estatus_disponibles,
            'es_creador': True,
            'container': True
        })
    
    else:
        try:
            # Procesar el formulario del proyecto
            form = ProyectoFormulario(request.POST, request.FILES, instance=task)
            formset_imagenes = ImagenesdeProyectoFormSetEditar(
                request.POST, 
                request.FILES, 
                queryset=ImagenesdeProyecto.objects.filter(proyecto=task)
            )
            
            if form.is_valid() and formset_imagenes.is_valid():
                # Guardar cambios en el proyecto
                proyecto = form.save(commit=False)

                # Actualizar el estatus seleccionado
                nuevo_estatus_id = request.POST.get('estatus')  # Obtener el ID del estatus seleccionado
                if nuevo_estatus_id:
                    nuevo_estatus = EstatusDeProyecto.objects.get(id=nuevo_estatus_id)
                    proyecto.estatus = nuevo_estatus

                proyecto.save()

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

                return redirect('task')

            else:
                # Mostrar los errores del formulario y del formset
                estatus_disponibles = EstatusDeProyecto.objects.all()
                return render(request, 'project_edit.html', {
                    'task': task,
                    'form': form,
                    'formset_imagenes': formset_imagenes,
                    'estatus_actual': task.estatus.id if task.estatus else None,
                    'estatus_disponibles': estatus_disponibles,
                    'error': "Error al actualizar el proyecto",
                    'form_errors': form.errors,
                    'formset_errors': formset_imagenes.errors,
                })

        except ValueError:
            estatus_disponibles = EstatusDeProyecto.objects.all()
            return render(request, 'project_edit.html', {
                'task': task,
                'form': form,
                'formset_imagenes': formset_imagenes,
                'estatus_actual': task.estatus.id if task.estatus else None,
                'estatus_disponibles': estatus_disponibles,
                'error': "Error al actualizar proyecto"
            })

@check_profile_completion
@verificar_usuario_bloqueado
def Proyectos_publicado(request):
    task = Proyecto.objects.filter(estatus__nombre='Activo').order_by('-FechaDeAgregado')
    return render(request, 'task_publicados.html', {'task': task, 'container': True})

@check_profile_completion
@login_required(login_url='loginkl')
@usuario_tipo_permitido(tipos_permitidos=['Admin', 'Empleado'])
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

# Exportador de PDF de proyectos para usuarios registrados
@login_required
@usuario_tipo_permitido(tipos_permitidos=['Admin', 'Empleado', 'Cliente'])
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

    # Descripción con saltos de línea respetados
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, "Descripción:")
    y_position -= 20
    p.setFont("Helvetica", 12)

    description = proyecto.descripcion
    lines = description.split('\n')  # Dividir la descripción en líneas según los saltos de línea originales
    for paragraph in lines:
        wrapped_text = wrap(paragraph, 80)  # Ajustar el ancho de cada párrafo
        for line in wrapped_text:
            if y_position < 100:
                p.showPage()
                add_watermark()
                draw_header_footer()
                y_position = height - 100
            p.drawString(50, y_position, line)
            y_position -= 15
        y_position -= 10  # Añadir espacio entre párrafos


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


def descargar_proyecto_pdf_visitantes(request, project_id):
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

    # Descripción con saltos de línea respetados
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, "Descripción:")
    y_position -= 20
    p.setFont("Helvetica", 12)

    description = proyecto.descripcion
    lines = description.split('\n')  # Dividir la descripción en líneas según los saltos de línea originales
    for paragraph in lines:
        wrapped_text = wrap(paragraph, 80)  # Ajustar el ancho de cada párrafo
        for line in wrapped_text:
            if y_position < 100:
                p.showPage()
                add_watermark()
                draw_header_footer()
                y_position = height - 100
            p.drawString(50, y_position, line)
            y_position -= 15
        y_position -= 10  # Añadir espacio entre párrafos


    # Finalizar el PDF
    p.showPage()
    p.save()
    return response



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

    # Manejar los filtros
    if filtro == 'all':
        proyectos = Proyecto.objects.all().order_by('-FechaDeAgregado')
    else:
        try:
            # Convertir el filtro a un entero y buscar el estatus correspondiente
            estatus = EstatusDeProyecto.objects.get(id=int(filtro))
            proyectos = Proyecto.objects.filter(estatus=estatus).order_by('-FechaDeAgregado')
        except (EstatusDeProyecto.DoesNotExist, ValueError):
            proyectos = Proyecto.objects.none()  # Sin resultados si el filtro es inválido

    # Escribir los proyectos en el CSV
    for proyecto in proyectos:
        empleado = proyecto.Empleado_Responsable
        # Generar el nombre del autor
        autor = (
            f"{empleado.first_name} {empleado.last_name}".strip()
            if empleado.first_name or empleado.last_name
            else empleado.username
        )
        # Formatear la fecha
        fecha_local = localtime(proyecto.FechaDeAgregado).strftime('%d/%m/%Y')

        writer.writerow([
            proyecto.id,
            proyecto.titulo,
            proyecto.descripcion,
            fecha_local,
            proyecto.estatus.nombre,
            autor
        ])

    return response


#Perfil de usuario registrado

@check_profile_completion
@usuario_tipo_permitido(tipos_permitidos=['Admin', 'Empleado', 'Cliente'])
@login_required(login_url='loginkl')  
def perfil(request):
    return render(request, 'profile.html', {'usuario': request.user, 'container': True})

#Editar perfil

@check_profile_completion
@verificar_usuario_bloqueado
@usuario_tipo_permitido(tipos_permitidos=['Admin', 'Empleado', 'Cliente'])
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

def error_permisos(request):
    return render(request, 'error_de_permisos.html', {'mensaje': 'No tienes permiso para acceder a esta página.'})


@usuario_tipo_permitido(tipos_permitidos=['Admin'])
@login_required
def admin_panel(request):
    return render(request, 'admin_panel.html', {'container': True})

@usuario_tipo_permitido(tipos_permitidos=['Admin'])
@login_required
def listar_usuarios(request):
    usuarios = User.objects.all().select_related('profile')  # Para optimizar consultas
    usuarios_con_grupos = [
        {
            'usuario': usuario,
            'grupos': ', '.join(grupo.name for grupo in usuario.groups.all()) or "Bloqueado"
        }
        for usuario in usuarios
    ]
    return render(request, 'admin_list_users.html', {'usuarios_con_grupos': usuarios_con_grupos})

@usuario_tipo_permitido(tipos_permitidos=['Admin'])
@login_required
def detalle_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    perfil = usuario.profile  # Relación OneToOne con UserProfile
    return render(request, 'admin_user_detail.html', {'usuario': usuario, 'perfil': perfil})

@usuario_tipo_permitido(tipos_permitidos=['Admin'])
def buscar_usuarios(request):
    query = request.GET.get('q', '').strip()  # Obtener y limpiar el término de búsqueda
    filtro = request.GET.get('filtro', 'todos').strip().lower()  # Asegurar formato consistente

    # Filtro base: todos los usuarios
    usuarios = User.objects.all()

    # Aplicar el filtro de búsqueda
    if query:
        usuarios = usuarios.filter(
            Q(username__icontains=query) |  # Buscar por username
            Q(first_name__icontains=query) |  # Buscar por primer nombre
            Q(last_name__icontains=query)  # Buscar por apellido
        )

    # Aplicar el filtro por tipo de usuario
    if filtro != 'todos':
        if filtro == 'bloqueados':
            usuarios = usuarios.filter(groups__isnull=True)  # Usuarios sin grupo
        else:
            usuarios = usuarios.filter(groups__name__iexact=filtro)  # Usuarios con un grupo específico (insensible a mayúsculas)

    usuarios_con_grupos = []
    for usuario in usuarios:
        grupos = ', '.join([group.name for group in usuario.groups.all()]) or 'Bloqueado'
        usuarios_con_grupos.append({'usuario': usuario, 'grupos': grupos})

    return render(request, 'admin_list_users.html', {
        'usuarios_con_grupos': usuarios_con_grupos,  # Procesados con grupos
        'query': query,
        'filtro': filtro,
        'tipos_usuarios': ['todos', 'Admin', 'Empleado', 'Cliente', 'bloqueados'],  # Tipos de usuario disponibles
    })
