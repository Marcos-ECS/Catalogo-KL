from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.forms import modelformset_factory
from .models import Proyecto, ImagenesdeProyecto, UserProfile
from django import forms
from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError



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


class RegistroFormulario(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")
    tipo_usuario = forms.ChoiceField(choices=UserProfile.TIPOS_USUARIO, label="Tipo de Usuario")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)  # Validar la contraseña
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
            return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Asignar al grupo según el tipo de usuario
            tipo_usuario = self.cleaned_data['tipo_usuario']
            group = Group.objects.get(name=tipo_usuario)  # Esto asume que los grupos ya existen
            user.groups.add(group)
        return user


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