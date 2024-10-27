from django.contrib import admin
from .models import Proyecto, ImagenesdeProyecto

# Registrar ImagenProyecto como inline en Proyecto
class ImagenesdeProyectoInline(admin.TabularInline):
    model = ImagenesdeProyecto
    extra = 3  # Número de imágenes adicionales que se pueden subir por defecto
    verbose_name_plural = 'Galería de proyecto'

class ProyectoAdmin(admin.ModelAdmin):
    inlines = [ImagenesdeProyectoInline]  # Añadir ImagenProyecto como inline en Proyecto

# Register your models here.
admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(ImagenesdeProyecto)