from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import UserManager
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractBaseUser,PermissionsMixin):
    #ID annadida por django por defecto
    nombre = models.CharField(max_length=100,blank=False)
    apellido = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=255, unique= True)
    password = models.CharField(max_length=200)
    #imagenPerfil = models.ImageField(upload_to='pfp',default="planky.png",null=True,blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre'] #email & password estan por default
    
    objects = UserManager()
    
    @property
    def nombreCompleto(self):
        return '%s %s' % (self.nombre, self.apellido)
    
class Trader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    edad = models.IntegerField(blank=True, null=True)
    intercambios = models.IntegerField(default=0)

class Ubicacion(models.Model):
    pais = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    estado = models.CharField(max_length=100, blank=True)

class Review(models.Model):
    trader = models.ForeignKey('Trader', on_delete=models.CASCADE, null=True)
    opinion = models.CharField(max_length=200)
    stars = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ],
        default=0
    )

CONDITION_CHOICES = (
    ('MALA','MALA'),
    ('BUENA', 'BUENA'),
    ('COMO NUEVO','COMO NUEVO'),
    ('NUEVO','NUEVO'),
)

CATEGORIA_CHOICES = (
    ('TALENTO/CONOCIMIENTO','TALENTO/CONOCIMIENTO'),
    ('OBJETO MATERIAL', 'OBJETO MATERIAL'),
    ('SERVICIO','SERVICIO'),
)

class Trade(models.Model):
    trader = models.ForeignKey('Trader', on_delete=models.CASCADE, null=True)
    titulo = models.CharField(max_length=100, default="Trade Producto")
    categoria = models.CharField(max_length=200,choices=CATEGORIA_CHOICES, default="")
    condicion = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='BUENA')
    descripcion = models.CharField(max_length=200, default="")
    intercambio_preferente = models.CharField(max_length=200, default="")
    is_active = models.BooleanField(default=True)
    image = models.ImageField(null=True)