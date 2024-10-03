from django.db import models
######################################################################################
# importacion de los modelos de los estudiantes
from estudiante.models import ModelAnteproyecto, ModelProyectoFinal, ModelAsignacionJurados
######################################################################################
######################################################################################
# importacion de los modelos de los estudiantes
from login.models import Usuarios
######################################################################################


# creacion del modelo de retroalimentaciones


class ModelRetroalimentaciones(models.Model):
    ESTADOS_CHOICES = [
        ('Aprobado', 'Aprobado'),
        ('Rechazado', 'Rechazado'),
    ]

    anteproyecto = models.ForeignKey(
        ModelAnteproyecto, on_delete=models.CASCADE, related_name='Retroalimentaciones', blank=True, null=True)
    user = models.ForeignKey(Usuarios, on_delete=models.SET_NULL,
                             related_name='Retroalimentaciones', blank=True, null=True)
    proyecto_final = models.ForeignKey(
        ModelProyectoFinal, on_delete=models.CASCADE, related_name='Retroalimentaciones', blank=True, null=True)
    retroalimentacion = models.TextField(
        max_length=10000)
    fecha_retroalimentacion = models.DateTimeField(blank=True, null=True)
    doc_retroalimentacion = models.BinaryField(null=True, blank=True)
    estado = models.CharField(
        max_length=25, choices=ESTADOS_CHOICES, default='aprobado', null=True, blank=True)
    revs_dadas = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if self.anteproyecto:
            return f"{self.anteproyecto.nombre_anteproyecto} - {self.estado}"
        else:
            return f"Solicitud eliminada - {self.estado}"

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

# creacion del modelo de solicitudes para el cambio de infromacion respecto al proyecto


class ModelSolicitudes(models.Model):
    TIPO_SOLICITUD = [
        ('cambio_nombre', 'Cambio de nombre del proyecto'),
        ('ajuste_integrantes', 'Ajuste de integrantes del proyecto'),
        ('seccion_derechos', 'Sección de derechos del proyecto'),
        ('otro', 'Otro'),
    ]

    user = models.ForeignKey(Usuarios, on_delete=models.CASCADE,
                             related_name='Solicitudes', blank=True, null=True)
    anteproyecto = models.ForeignKey(
        ModelAnteproyecto, on_delete=models.CASCADE, blank=True, null=True, related_name='Solicitudes')
    proyecto_final = models.ForeignKey(
        ModelProyectoFinal, on_delete=models.CASCADE, blank=True, null=True, related_name='Solicitudes')
    retroalimentaciones = models.ForeignKey(
        ModelRetroalimentaciones, on_delete=models.CASCADE, blank=True, null=True, related_name='Solicitudes')
    tipo_solicitud = models.CharField(
        max_length=200, choices=TIPO_SOLICITUD, default='otro',)
    motivo_solicitud = models.TextField(max_length=10000)
    documento_soporte = models.BinaryField(blank=True, null=True)
    fecha_envio = models.DateTimeField(blank=True, null=True)
    estado = models.BooleanField(default=False)


# creacion del modelo de los documentos
class ModelDocumentos(models.Model):
    nombre_documento = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    documento = models.BinaryField(blank=True, null=True)
    fecha_cargue = models.DateTimeField(blank=True, null=True)
