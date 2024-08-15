from django.db import models

# importacion de maximos y minimos validadores en el campo de integerfield
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


# Creacion del modelo del estudiante para el login
class Estudiante(models.Model):
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100)
    semestre_curso = models.IntegerField()
    user_email = models.CharField(max_length=100)
    contraseña = models.IntegerField()


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
