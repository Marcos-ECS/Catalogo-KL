from apps.signupKL.models import LoginLog


def obtener_ip_dispositivo(request):
    """
    Obtiene la dirección IP del cliente y el dispositivo desde el request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def registrar_login(usuario, ip_address=None, dispositivo=None):
    """
    Registra un inicio de sesión en el modelo LoginLog.
    """
    LoginLog.objects.create(usuario=usuario, ip_address=ip_address, dispositivo=dispositivo)
