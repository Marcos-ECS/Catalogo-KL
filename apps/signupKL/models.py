from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import Group


# Modelo de Estatus de Proyecto
class EstatusDeProyecto(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#6C757D')  # Hexadecimal para el color
    descripcion = models.TextField(blank=True, null=True)  # Opcional: para documentar el propósito del estatus

    def __str__(self):
        return self.nombre

# Modelo de Proyecto
class Proyecto(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(
        blank=False,
        null=False,
        max_length=1000,
        validators=[MinLengthValidator(50)]
    )
    FechaDeAgregado = models.DateTimeField(auto_now_add=True)
    Fecha_De_Realizacion = models.DateTimeField(null=True, blank=True)
    estatus = models.ForeignKey(EstatusDeProyecto, on_delete=models.SET_NULL, null=True, blank=True, related_name='proyectos')
    Empleado_Responsable = models.ForeignKey(User, on_delete=models.CASCADE)
    Portada_de_proyecto = models.ImageField(upload_to='proyectos_portada/', blank=False, null=True)

    def __str__(self):
        return self.titulo

# Modelo de Galería de Imágenes
class ImagenesdeProyecto(models.Model):
    proyecto = models.ForeignKey(Proyecto, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='proyectos_galeria/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Galería de proyectos'

    def __str__(self):
        return f"Galeria para {self.proyecto.titulo}"

# Modelo de Perfil de Usuario
class UserProfile(models.Model):
    TIPOS_USUARIO = [
        ('Empleado', 'Empleado'),
        ('Admin', 'Admin'),
        ('Cliente', 'Cliente'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='Empleado')
    ultimo_grupo = models.ForeignKey(
        Group, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='usuarios_recuperados',
        verbose_name='Último grupo asignado'
    )
    
    def __str__(self):
        return f"Perfil de {self.user.username} ({self.tipo_usuario})"

#Modelo de logs de inicio de sesion
class LoginLog(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    dispositivo = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.fecha_hora}"

#Modelo de logs de edicion de proyectos
class ProyectoLog(models.Model):
    ACCIONES = [
        ('creado', 'Creado'),
        ('editado', 'Editado'),
        ('estatus', 'Cambio de Estatus'),
    ]

    proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=20, choices=ACCIONES)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.proyecto.titulo} - {self.accion} por {self.usuario.username if self.usuario else 'Sistema'}"
