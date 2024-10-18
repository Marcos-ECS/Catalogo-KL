from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Proyecto(models.Model):
    Estatus_de_proyecto = [
        ('Si', 'Activo'),
        ('No', 'Inactivo'),
    ]

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    FechaDeAgregado = models.DateTimeField(auto_now_add=True)
    Fecha_De_Realizacion = models.DateTimeField(null=True, blank=True)
    Estatus_de_proyecto = models.CharField(max_length=2, choices=Estatus_de_proyecto, default='No')
    Empleado_Responsable = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo