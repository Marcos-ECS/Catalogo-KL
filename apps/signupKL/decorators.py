from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps


def usuario_visitante(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func (request, *args, **kwargs)
        
def usuarios_permitidos(usuarios_permitidos=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group=None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in usuarios_permitidos:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Vista no permitida')
        return wrapper_func
    return decorator

def check_profile_completion(view_func):
    """
    Decorador que verifica si el perfil del usuario está completo y agrega un mensaje si no lo está.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Obtener el perfil del usuario
            profile = request.user.profile
            # Verificar si los datos del usuario están completos
            is_complete = all([
                request.user.first_name,  # Esto está en el modelo User
                request.user.last_name,
                request.user.email,
                profile.photo  # Esto está en el modelo UserProfile
            ])
            # Establecer la variable de sesión
            request.session['profile_incomplete'] = not is_complete

        return view_func(request, *args, **kwargs)
    return wrapper