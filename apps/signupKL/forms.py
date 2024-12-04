from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from .models import Proyecto, ImagenesdeProyecto, UserProfile
from django import forms
from django.utils.translation import gettext_lazy as _ 



class ProyectoFormulario(ModelForm):
    class Meta:
        model = Proyecto
        fields = ['titulo', 'Portada_de_proyecto','descripcion', 'estatus']

    def __init__(self, *args, **kwargs):
        super(ProyectoFormulario, self).__init__(*args, **kwargs)
        # Excluir 'Estatus_de_proyecto' si el formulario es para crear un proyecto
        if kwargs.get('instance') is None:  # Es un proyecto nuevo (no existe instancia)
            self.fields.pop('estatus')

        def clean_descripcion(self):
            descripcion = self.cleaned_data.get('descripcion')
            if len(descripcion) < 50:
                raise forms.ValidationError("La descripción debe tener al menos 50 caracteres.")
            return descripcion
    
    
# Formset para crear proyectos (sin opción de eliminar)
ImagenesdeProyectoFormSetCrear = modelformset_factory(
    ImagenesdeProyecto,
    fields=('imagen',),
    extra=3,  # Ajustar extra según sea necesario
    can_delete=False  # No permitir eliminación en la creación
)


ImagenesdeProyectoFormSetEditar = modelformset_factory(
    ImagenesdeProyecto,
    fields=('imagen',),
    extra=1,
    can_delete=True,
    widgets={
        'imagen': forms.ClearableFileInput(attrs={'required': False})  # Hacer el campo no requerido
    }
)

# formset para proyectos en donde el usuario no es el autor
ImagenesdeProyectoFormSetSoloLectura = modelformset_factory(
    ImagenesdeProyecto,
    fields=('imagen',),
    extra=0,  # No agregar espacios adicionales
    can_delete=False  # No permitir eliminar en modo solo lectura
)


class RegistroFormulario(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': _('Nombre de usuario'),
            'password1': _('Contraseña'),
            'password2': _('Confirmar contraseña'),
        }
        help_texts = {
            'username': _('Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.'),
        }
        error_messages = {
            'username': {
                'unique': _('Este nombre de usuario ya está en uso.'),
            },
            'password_mismatch': _('Las contraseñas no coinciden.'),
        }
    def __init__(self, *args, **kwargs):
        super(RegistroFormulario, self).__init__(*args, **kwargs)
        self.fields['password1'].label = 'Contraseña'  # Cambia el label de password1
        self.fields['password2'].label = 'Confirmar contraseña'  # Cambia el label de password2


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # Solo incluye los campos que deseas mostrar
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo']  # Incluye la foto de perfil
        labels = {
            'photo': 'Foto de perfil',
        }
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }