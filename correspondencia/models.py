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
        ModelAnteproyecto, on_delete=models.SET_NULL, related_name='Asignacion_Jurados', blank=True, null=True)
    proyecto_final = models.ForeignKey(
        ModelProyectoFinal, on_delete=models.SET_NULL, related_name='Asignacion_Jurados', blank=True, null=True)
    nombre_jurado = models.CharField(max_length=50)
    fecha_sustentacion = models.DateField(max_length=50)

    def save(self,*args, **kwargs):
        super().save(*args,**kwargs)
# creacion del modelo de retroalimentaciones


class ModelRetroalimentaciones(models.Model):
    ESTADOS_CHOICES = [
        ('Aprobado', 'Aprobado'),
        ('Aprobado_con_correcciones', 'Aprobado con correcciones'),
        ('Rechazado', 'Rechazado'),
    ]

    anteproyecto = models.ForeignKey(
        ModelAnteproyecto, on_delete=models.SET_NULL, related_name='Retroalimentaciones', blank=True, null=True)
    proyecto_final = models.ForeignKey(
        ModelProyectoFinal, on_delete=models.SET_NULL, related_name='Retroalimentaciones', blank=True, null=True)
    jurado = models.ForeignKey(
        ModelAsignacionJurados, on_delete=models.SET_NULL, related_name='Retroalimentaciones', blank=True, null=True)

    retroalimentacion = models.TextField(
        max_length=10000)
    fecha_retroalimentacion = models.CharField(max_length=50)
    doc_retroalimentacion = models.BinaryField(null=True, blank=True)
    estado = models.CharField(
        max_length=25, choices=ESTADOS_CHOICES, default='aprobado')
    revs_dadas = models.IntegerField(null=True, blank=True)

    def __str__(self):
        if self.anteproyecto:
            return f"{self.anteproyecto.nombre_anteproyecto} - {self.estado}"
        else:
            return f"Solicitud eliminada - {self.estado}"

# creacion del modelo de informacion de entrega final


class ModelInformacionEntregaFinal(models.Model):
    anteproyecto = models.ForeignKey(
        ModelAnteproyecto, on_delete=models.SET_NULL, related_name='Informacion_Entrega_Final', blank=True, null=True)
    proyecto_final = models.ForeignKey(
        ModelProyectoFinal, on_delete=models.SET_NULL, related_name='Informacion_Entrega_Final', blank=True, null=True)
    jurado = models.ForeignKey(
        ModelAsignacionJurados, on_delete=models.SET_NULL, related_name='Informacion_Entrega_Final', blank=True, null=True)
    retroalimentaciones = models.ForeignKey(
        ModelRetroalimentaciones, on_delete=models.SET_NULL, related_name='Informacion_Entrega_Final', blank=True, null=True)

# creacion del modelo de solicitudes para el cambio de infromacion respecto al proyecto


class ModelSolicitudes(models.Model):
    TIPO_SOLICITUD = [
        ('cambio_nombre', 'Cambio de nombre del proyecto'),
        ('ajuste_integrantes', 'Ajuste de integrantes del proyecto'),
        ('seccion_derechos', 'Sección de derechos del proyecto'),
        ('otro', 'Otro'),
    ]

    RELACIONADO_CON_CHOICES = [
        ('anteproyecto', 'Anteproyecto'),
        ('proyecto_final', 'Proyecto Final'),
    ]

    user = models.ForeignKey(Usuarios, on_delete=models.SET_NULL,
                             related_name='Solicitudes', blank=True, null=True)
    anteproyecto = models.ForeignKey(
        ModelAnteproyecto, on_delete=models.SET_NULL, blank=True, null=True, related_name='Solicitudes')
    proyecto_final = models.ForeignKey(
        ModelProyectoFinal, on_delete=models.SET_NULL, blank=True, null=True, related_name='Solicitudes')
    relacionado_con = models.CharField(
        max_length=255,
        choices=RELACIONADO_CON_CHOICES)
    retroalimentaciones = models.ForeignKey(
        ModelRetroalimentaciones, on_delete=models.SET_NULL, blank=True, null=True, related_name='Solicitudes')
    tipo_solicitud = models.CharField(
        max_length=200, choices=TIPO_SOLICITUD, default='otro',)
    motivo_solicitud = models.TextField(max_length=10000)
    documento_soporte = models.BinaryField(blank=True, null=True)
    fecha_envio = models.CharField(max_length=50)
    estado = models.BooleanField(default=False)
