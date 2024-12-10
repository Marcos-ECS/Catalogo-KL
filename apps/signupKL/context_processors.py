from django.contrib.auth.models import Group

def navbar_context(request):
    """
    Context processor para gestionar la lógica del navbar basada en el tipo de usuario.
    """
    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        grupos_usuario = list(request.user.groups.values_list('name', flat=True))
        es_cliente = 'Cliente' in grupos_usuario
        es_empleado = 'Empleado' in grupos_usuario
        es_admin = 'Admin' in grupos_usuario
    else:
        es_cliente = es_empleado = es_admin = False

    return {
        'es_visitante': not request.user.is_authenticated,
        'es_cliente': es_cliente,
        'es_empleado': es_empleado,
        'es_admin': es_admin,
    }
