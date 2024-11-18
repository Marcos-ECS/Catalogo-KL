from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


# Create your models here.
class Proyecto(models.Model):
    Estatus_de_proyecto = [
        ('Si', 'Activo'),
        ('No', 'Inactivo'),
    ]

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(
        blank=False, 
        null=False, 
        max_length=1000, 
        validators=[MinLengthValidator(50)]  
    )
    FechaDeAgregado = models.DateTimeField(auto_now_add=True)
    Fecha_De_Realizacion = models.DateTimeField(null=True, blank=True)
    Estatus_de_proyecto = models.CharField(max_length=2, choices=Estatus_de_proyecto, default='No')
    Empleado_Responsable = models.ForeignKey(User, on_delete=models.CASCADE)
    Portada_de_proyecto = models.ImageField(upload_to='proyectos_portada/', blank=False, null=True)

    def __str__(self):
        return self.titulo
    
class ImagenesdeProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='proyectos_galeria/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Galería de proyectos' 
        
    def __str__(self):
        return f"Galeria para {self.proyecto.titulo}"
    
# Modelo de Perfil de Usuario
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"