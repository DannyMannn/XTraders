from django import forms
from django.forms import ModelForm, fields
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import authenticate

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('nombre','apellido','email')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = "<ul><li>Tu contraseña no puede ser demasiado parecida a tus otros datos personales.</li><li>Tu contraseña no puede ser una contraseña de uso común.</li><li>Tu contraseña debe contener al menos 8 caracteres.</li><li>Tu contraseña no puede ser totalmente numérica.</li></ul>"
        self.fields['password2'].help_text = "Introduzca la misma contraseña que antes, para la verificación."

class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()

    fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("No existe el usuario. Checa que los datos estén bien.")
        return self.cleaned_data