from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def signup(request):
    return render (request, 'signkl.html',{
        'form': UserCreationForm
    })