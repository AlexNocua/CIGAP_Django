# importacion de utilidades de django

from .models import Usuarios
from estudiante.models import Estudiante
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# importaciones para la creaciones de datos
# importacion de los models


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Usuarios
        fields = ('nombres', 'apellidos', 'email', 'password1', 'password2')

    def save(self, commit=True):
        
        user = super().save(commit=False)
        user.is_active = True
        # Asegura que la contraseña se encripte correctamente
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user




# creacion del formulario del registro


class FormRegistro(UserCreationForm):

    class Meta:
        model = Usuarios

        fields = ('nombres', 'apellidos', 'email', 'password1', 'password2')
        widgets = {
            'nombres': forms.TextInput(attrs={'placeholder': 'Digita tus nombres', 'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'placeholder': 'Digita tus apellidos', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@correo.com', 'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Contraseña mayor a 8 caracteres',
                'class': 'form-control',
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Repite la contraseña',
                'class': 'form-control',
            }),
        }

    # funcion para guardar el registro

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.nombres = self.cleaned_data["nombres"]
        user.apellidos = self.cleaned_data["apellidos"]

        if commit:
            user.save()
            estudiantes_group, created = Group.objects.get_or_create(
                name='Estudiantes')
            user.groups.add(estudiantes_group)
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # esto es para sobrescribir las configuraciones predeterminadas
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Contraseña mayor a 8 caracteres',
            'class': 'form-control',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Repite la contraseña',
            'class': 'form-control',
        })
