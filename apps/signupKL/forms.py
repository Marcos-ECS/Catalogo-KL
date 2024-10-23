from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from .models import Proyecto, ImagenesdeProyecto

class ProyectoFormulario(ModelForm):
    class Meta:
        model = Proyecto
        fields = ['titulo', 'Portada_de_proyecto','descripcion', 'Estatus_de_proyecto']

    def __init__(self, *args, **kwargs):
        super(ProyectoFormulario, self).__init__(*args, **kwargs)
        # Excluir 'Estatus_de_proyecto' si el formulario es para crear un proyecto
        if kwargs.get('instance') is None:  # Es un proyecto nuevo (no existe instancia)
            self.fields.pop('Estatus_de_proyecto')

ImagenesdeProyectoFormSet = modelformset_factory(ImagenesdeProyecto, fields=('imagen',), extra=3)  # Puedes ajustar 'extra'

class RegistroFormulario(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña'
        }
    def __init__(self, *args, **kwargs):
        super(RegistroFormulario, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Contraseña'  # Cambia el label de password1
        self.fields['password2'].label = 'Confirmar contraseña'  # Cambia el label de password2