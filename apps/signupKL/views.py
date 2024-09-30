from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login
from django.db import IntegrityError


# Create your views here.
#Registro de usuaurios
def signup(request):
    if request.method == 'GET':
        return render (request, 'signkl.html',{
        'form': UserCreationForm
        
    })
    else:
        if request.POST ['password1'] == request.POST['password2']:
            try:
                #registro
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('loginuser')   
            except IntegrityError:
                    return render (request, 'signkl.html',{
                    'form': UserCreationForm,
                    "error": 'El usuario ya existe'
                })
        return render(request, 'signkl.html',{
            'form': UserCreationForm,
            "error": 'La contraseña no coincide'
        })
    
def loginkl(request):
     return render(request, 'loginuser.html')