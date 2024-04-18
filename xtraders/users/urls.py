from django.urls import path,include
from . import views

from users import views
from django.contrib.auth.decorators import login_required


app_name = 'users'

urlpatterns = [
    path("",views.home,name="home"),
]