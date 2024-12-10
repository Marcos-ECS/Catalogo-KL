from django.shortcuts import render
from apps.signupKL.decorators import verificar_usuario_bloqueado, check_profile_completion
# Create your views here.
@check_profile_completion
@verificar_usuario_bloqueado
def home(request):
    return render(request, 'home.html')