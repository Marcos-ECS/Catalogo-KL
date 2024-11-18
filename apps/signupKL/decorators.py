from django.http import HttpResponse
from django.shortcuts import redirect

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