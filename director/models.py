from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# importacion de modelos del login
from login.models import Usuarios

# importacion de modelos de estudiante
from estudiante.models import ModelAnteproyecto, ModelProyectoFinal
# creacion del modelo de evaluador


class ModelEvaluacionAnteproyecto(models.Model):
    evaluador = models.ForeignKey(Usuarios, on_delete=models.CASCADE,
                                  related_name='evaluacion_anteproyectos', blank=True, null=True)
    anteproyecto = models.ForeignKey(
        ModelAnteproyecto, on_delete=models.CASCADE, related_name='evaluacion_anteproyectos', blank=True, null=True)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)
    comentarios = models.CharField(max_length=10000, blank=True, null=True)
    fecha_evaluacion = models.DateField(auto_now_add=True)


# creacion del modelo de evaluador de jurado
class ModelEvaluacionProyectoFinal(models.Model):
    evaluador = models.ForeignKey(Usuarios, on_delete=models.CASCADE,
                                  related_name='evaluacion_proyectos', blank=True, null=True)
    proyecto_final = models.ForeignKey(
        ModelProyectoFinal, on_delete=models.CASCADE, related_name='evaluacion_proyectos', blank=True, null=True)
    calificacion = models.DecimalField(max_digits=5, decimal_places=2)
    comentarios = models.CharField(max_length=10000, blank=True, null=True)
    fecha_evaluacion = models.DateField(auto_now_add=True)
