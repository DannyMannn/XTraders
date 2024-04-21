from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Ubicacion, Trader

from django.http import HttpResponse

from .forms import UserLoginForm, UserRegistrationForm


def home(request):
    return render(request, "users/home.html")

def trade(request):
    return render(request, "users/trade.html")

def about(request):
    return render(request, "users/about.html")


def signup(request):
    if request.method == "POST":
        registro = UserRegistrationForm(request.POST) #get the form filled out 
        if registro.is_valid():
            newUser = registro.save(commit=False)
            newUser.save()

            # Create related Trader object
            trader = Trader.objects.create(user=newUser)
            
            # Create related Ubicacion object
            ubicacion = Ubicacion.objects.create(user=newUser)
                
            login(request,newUser)
            return redirect('users:home')
    else:
        registro = UserRegistrationForm()
    return render(request, "users/signup.html", {"registro":registro})

def signin(request):
    return render(request, "users/login.html")

def signout(request):
    logout(request)
    return redirect("users:home")