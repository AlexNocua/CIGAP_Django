from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser


# manejo de errores
import datetime


class ModelError(models.Model):
    estado = models.IntegerField()
    fecha_hora_error = models.DateTimeField()


class Usuarios(AbstractUser):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Cambiado a EmailField para validación adicional
    username = None  # Eliminamos el campo username de AbstractUser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombres', 'apellidos']

    def __str__(self):
        return self.email