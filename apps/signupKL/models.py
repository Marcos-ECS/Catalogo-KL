from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Proyecto(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    FechaDeAgregado = models.DateTimeField(auto_now_add=True)
    Fecha_De_Realizacion = models.DateTimeField(null=True)
    importante = models.BooleanField(default=False)
    Empleado_Responsable = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo