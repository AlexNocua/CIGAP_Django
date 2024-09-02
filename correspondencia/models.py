from django.db import models
from estudiante.models import ModelAnteproyecto
# Create your models here.


class ModelRetroalimentacionesAnteproyecto(models.Model):
    ESTADOS_CHOICES = [
        ('aprobado', 'Aprobado'),
        ('aprobado_con_correcciones', 'Aprobado con correcciones'),
        ('rechazado', 'Rechazado'),
    ]

    anteproyecto = models.ForeignKey(
        ModelAnteproyecto, on_delete=models.CASCADE, related_name='retroalimentaciones')
    retroalimentacion = models.TextField(max_length=1000)
    fecha_retroalimentacion = models.CharField(max_length=50)
    doc_retroalimentacion = models.BinaryField(null=True, blank=True)
    estado = models.CharField(max_length=25, choices=ESTADOS_CHOICES, default='aprobado')
    revs_dadas = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.anteproyecto.nombre_anteproyecto} - {self.estado}"
