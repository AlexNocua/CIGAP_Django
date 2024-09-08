from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser


# manejo de errores
import datetime

# importacion de managers con el fin de gestionar la creacion de supeusuarios de manera correcta
from .managers import UserManager


class ModelError(models.Model):
    estado = models.IntegerField()
    fecha_hora_error = models.DateTimeField()


class Usuarios(AbstractUser):
    ROLES_CHOICES = (
        ('estudiante', 'Estudiante'),
        ('director', 'Director'),
        ('correspondencia', 'Correspondencia'),
    )

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    nombre_completo = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique=True)
    username = None  # Eliminamos el campo username de AbstractUser
    imagen = models.BinaryField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombres', 'apellidos']

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.nombre_completo = f"{self.nombres} {self.apellidos}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


