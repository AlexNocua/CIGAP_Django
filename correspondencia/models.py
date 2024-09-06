from django.db import models
######################################################################################
# importacion de los modelos de los estudiantes
from estudiante.models import ModelAnteproyecto, ModelProyectoFinal
######################################################################################
######################################################################################
# importacion de los modelos de los estudiantes
from login.models import Usuarios
######################################################################################


# creacion del modelo de jurados
class ModelAsignacionJurados(models.Model):
    usuario = models.ForeignKey(
        ModelAnteproyecto, on_delete=models.CASCADE, related_name='Asignacion_Jurados', blank=True, null=True)
    proyecto_final = models.ForeignKey(
        ModelProyectoFinal, on_delete=models.CASCADE, related_name='Asignacion_Jurados', blank=True, null=True)
    nombre_jurado = models.CharField(max_length=50)
    fecha_sustentacion = models.CharField(max_length=50)

# creacion del modelo de retroalimentaciones


class ModelRetroalimentaciones(models.Model):
    ESTADOS_CHOICES = [
        ('Aprobado', 'Aprobado'),
        ('Aprobado_con_correcciones', 'Aprobado con correcciones'),
        ('Rechazado', 'Rechazado'),
    ]

    anteproyecto = models.ForeignKey(
        ModelAnteproyecto, on_delete=models.CASCADE, related_name='Retroalimentaciones', blank=True, null=True)
    proyecto_final = models.ForeignKey(
        ModelProyectoFinal, on_delete=models.CASCADE, related_name='Retroalimentaciones', blank=True, null=True)
    jurado = models.ForeignKey(
        ModelAsignacionJurados, on_delete=models.CASCADE, related_name='Retroalimentaciones', blank=True, null=True)

    retroalimentacion = models.TextField(
        max_length=10000)
    fecha_retroalimentacion = models.CharField(max_length=50)
    doc_retroalimentacion = models.BinaryField(null=True, blank=True)
    estado = models.CharField(
        max_length=25, choices=ESTADOS_CHOICES, default='aprobado')
    revs_dadas = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.anteproyecto.nombre_anteproyecto} - {self.estado}"


# creacion del modelo de informacion de entrega final
class ModelInformacionEntregaFinal(models.Model):
    anteproyecto = models.ForeignKey(
        ModelAnteproyecto, on_delete=models.CASCADE, related_name='Informacion_Entrega_Final', blank=True, null=True)
    proyecto_final = models.ForeignKey(
        ModelProyectoFinal, on_delete=models.CASCADE, related_name='Informacion_Entrega_Final', blank=True, null=True)
    jurado = models.ForeignKey(
        ModelAsignacionJurados, on_delete=models.CASCADE, related_name='Informacion_Entrega_Final', blank=True, null=True)
    retroalimentaciones = models.ForeignKey(
        ModelRetroalimentaciones, on_delete=models.CASCADE, related_name='Informacion_Entrega_Final', blank=True, null=True)
