from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from .forms import LoginFormulario

# Vista de login
def loginkl(request):
    if request.method == 'GET':
        return render(request, 'loginkl.html', {
            'form': LoginFormulario(),
            'container': True
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'loginkl.html', {
                'form': LoginFormulario(),
                'error': 'Usuario o contraseña incorrecta',
                'container': True
            })
        else:
            login(request, user)

            # Verificar el grupo del usuario y redirigir según corresponda
            if user.groups.filter(name='Admin').exists():
                return redirect('admin_panel')  # Redirige al panel de administración
            elif user.groups.filter(name='Empleado').exists():
                return redirect('task')  # Redirige al menú de proyectos
            elif user.groups.filter(name='Cliente').exists():
                return redirect('published_projects')  # Redirige a proyectos publicados
            else:
                return redirect('home')  # Redirige al home si no pertenece a ningún grupo
