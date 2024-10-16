from django.forms import ModelForm
from .models import Proyecto

class ProyectoFormulario(ModelForm):
    class Meta:
        model = Proyecto
        fields = ['titulo', 'descripcion', 'Publicar']