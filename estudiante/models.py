from django.db import models
from django import forms
import base64

# importacion de maximos y minimos validadores en el campo de integerfield
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# esta es para la creacion de usuarion personalizados, sin embargo con las caracteristicas de DJANGO
from django.contrib.auth.models import AbstractUser
# Creacion del modelo del estudiante para el login


from django.contrib.auth.models import Group
from login.models import Usuarios



# creacion del modelo para guardar los datos del anteproyecto
class ModelAnteproyecto(models.Model):
    
    user = models.ForeignKey(
        Usuarios, on_delete=models.CASCADE, related_name='Anteproyecto', blank = True,null = True)
    nombre_anteproyecto = models.CharField(max_length=200)
    nombre_integrante1 = models.CharField(max_length=200)
    nombre_integrante2 = models.CharField(
        max_length=200, null=True, blank=True)  # Cambio aquí
    descripcion = models.TextField(
        max_length=10000, null=True, blank=True)  # Cambio aquí
    carta_presentacion = models.BinaryField(null=True, blank=True)
    anteproyecto = models.BinaryField(null=True, blank=True)
    director = models.CharField(max_length=200, null=True)
    codirector = models.CharField(
        max_length=200, null=True, blank=True)  # Cambio aquí
    fecha_envio = models.CharField(max_length=200)

    # estas son modificadas por correspondencia
    solicitud_enviada = models.BooleanField()


# creacion del modelo de monografia o proyecto de grado
class ModelProyectoFinal(models.Model):
    user = models.OneToOneField(
        Usuarios, on_delete=models.CASCADE, related_name='Proyecto_Final', blank = True,null = True)
    anteproyecto = models.OneToOneField(
        ModelAnteproyecto, on_delete=models.CASCADE, related_name='Proyecto_Final', blank = True,null = True)
    descripcion = models.TextField(
        max_length=10000, null=True, blank=True)  # Cambio aquí
    carta_presentacion_final = models.BinaryField(null=True, blank=True)
    proyecto_final = models.BinaryField(null=True, blank=True)
    director = models.CharField(max_length=200, null=True)
    codirector = models.CharField(max_length=200, null=True)
    fecha_envio = models.CharField(max_length=200)
    solicitud_enviada = models.BooleanField()
