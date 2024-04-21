from django.urls import path,include
from . import views

from users import views
from django.contrib.auth.decorators import login_required


app_name = 'users'

urlpatterns = [
    path("",views.home,name="home"),
    path("trade",views.trade,name="trade"),
    path("about",views.about,name="about"),
    path("signup",views.signup,name="signup"),
    path("signin",views.signin,name="signin"),
    path("signout",views.signout,name="signout"),
]