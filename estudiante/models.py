from django.db import models
from django import forms


# importacion de maximos y minimos validadores en el campo de integerfield
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# esta es para la creacion de usuarion personalizados, sin embargo con las caracteristicas de DJANGO
from django.contrib.auth.models import AbstractUser
# Creacion del modelo del estudiante para el login


from django.contrib.auth.models import Group




class Estudiante(models.Model):
    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    email = models.EmailField(
        max_length=100, unique=True, verbose_name='Correo')


    # Otros campos y métodos que necesites

# creacion del modelo de primera solicitud.

#!funcionando


class ModelPrimeraSolicitud(models.Model):
    tematica = models.CharField(
        verbose_name='Inscribe la temática a tratar', max_length=1000)

    LINEAS_INVESTIGACION_CHOICES = [
        ('IA', 'Inteligencia Artificial'),
        ('BD', 'Bases de Datos'),
        ('RS', 'Redes y Seguridad'),
        ('SI', 'Sistemas de Información'),
        ('DS', 'Desarrollo de Software'),
    ]

    lineas_inv = models.CharField(
        verbose_name='Selecciona a que línea de investigación pertenece el proyecto',
        max_length=255,
        choices=LINEAS_INVESTIGACION_CHOICES
    )

    problema = models.TextField(
        verbose_name='Problemática para tratar (máximo 500 palabras)',
    )

    NUM_INTEGRANTES_CHOICES = [
        ('1', '1 Integrante'),
        ('2', '2 Integrantes'),
    ]

    num_integrantes = models.CharField(
        verbose_name='Selecciona el número de integrantes (máximo 2)',
        max_length=1,
        choices=NUM_INTEGRANTES_CHOICES
    )

    def clean(self):
        # Validar que el problema no sea mayor a 500 palabras
        palabra_count = len(self.problema.split())
        if palabra_count > 500:
            raise ValidationError({
                'problema': f'La problemática no puede tener más de 500 palabras, tiene {palabra_count}.'
            })

# creacion del modelo para guardar los datos del anteproyecto


class Anteproyecto (models.Model):
    nombre_proyecto = models.CharField(max_length=200)
    num_integrantes = models.IntegerField(
        validators=[MaxValueValidator(2), MinValueValidator(2)])
    carta_presentacion = models.FileField()
    anteproyecto = models.FileField()
    num_solicitud_anteproyecto = models.IntegerField()
    estado_solicitud_anteproyecto = models.BooleanField()
    director = models.CharField(max_length=200)
    coodirector = models.CharField(max_length=200)


# creacion del modelo de monografia o proyecto de grado
class ProyectoGrado (models.Model):
    pass


class EtapasProyecto (models.Model):
    pass


# creacion del modelo mas grande respecto a relaciones con otras aplicaciones
# Modelo de Observaciones

class Observaciones (models.Model):
    pass
