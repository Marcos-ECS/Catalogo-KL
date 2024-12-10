from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps


def usuario_visitante(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func (request, *args, **kwargs)
        
def usuario_tipo_permitido(tipos_permitidos=[], redirect_url='error_permisos'):
    """
    Decorador para restringir acceso basado en grupos.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name  # Obtiene el nombre del grupo del usuario
            
            if group in tipos_permitidos:
                return view_func(request, *args, **kwargs)
            else:
                return redirect(redirect_url)
        return wrapper_func
    return decorator



def check_profile_completion(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Verificar si el usuario está bloqueado
            if request.user.groups.exists():
                profile = request.user.profile
                is_complete = all([
                    request.user.first_name,
                    request.user.last_name,
                    request.user.email,
                    profile.photo
                ])
                request.session['profile_incomplete'] = not is_complete
            else:
                # Eliminar el mensaje si está bloqueado
                request.session.pop('profile_incomplete', None)

        return view_func(request, *args, **kwargs)
    return wrapper



def verificar_usuario_bloqueado(view_func):
    """
    Decorador para verificar si el usuario está bloqueado (sin grupos).
    Si está bloqueado, se muestra un mensaje de advertencia.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.groups.exists():
            # Usuario sin grupos: marcar como bloqueado en la sesión
            request.session['usuario_bloqueado'] = True
        else:
            # Usuario con grupos: limpiar mensaje de bloqueado si existe
            request.session.pop('usuario_bloqueado', None)

        return view_func(request, *args, **kwargs)
    return wrapper
