from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import LoginFormulario
# Create your views here.
def loginkl(request):
    if request.method == 'GET':
        return render(request, 'loginkl.html',{
        'form': LoginFormulario(), 'container': True 
    })
    else:
        user=authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginkl.html', {
                'form': LoginFormulario(),
                'error': 'Usuario o contraseña incorrecta', 'container': True 
            })
        else:
            login(request, user)
            return redirect ('task')