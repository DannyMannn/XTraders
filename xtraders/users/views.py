from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Ubicacion, Trader, Trade

from django.http import HttpResponse

from .forms import UserLoginForm, UserRegistrationForm, TradeForm


def home(request):
    return render(request, "users/home.html")

@login_required
def trade(request):
    trades = Trade.objects.all()

    return render(request, "users/trade.html", {"trades":trades})

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
    signinForm = UserLoginForm(request.POST or None)
    if signinForm.is_valid():
        email = signinForm.cleaned_data['email']
        password = signinForm.cleaned_data['password']
        user = authenticate(request, email=email,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('users:home')
        else: #User doesn't exist
            signinForm = UserLoginForm()
            return render(request,"users/login.html",{"signinForm":signinForm})  
    return render(request,"users/login.html",{"signinForm":signinForm })

def signout(request):
    logout(request)
    return redirect("users:home")

@login_required
def registerTrade(request):
    user = request.user
    tradeForm = TradeForm()

    if request.method == "POST":
        tradeForm = TradeForm(request.POST, request.FILES)
        if tradeForm.is_valid():
            newTrade = tradeForm.save(commit=False)
            newTrade.trader = user.trader
            newTrade.save()
            return redirect('users:trade')
        else:
            return render(request, "users/registerTrade.html", {"tradeForm": tradeForm})
    else:
        return render(request, "users/registerTrade.html", {"tradeForm": tradeForm})