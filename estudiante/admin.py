import base64
from .models import ModelAnteproyecto
from django.contrib import admin

# Para conseguir renderizar componentes en el admin
from django.utils.html import format_html

from .models import Estudiante, ModelAnteproyecto
# Register your models here.

admin.site.register(Estudiante)

# Revisar esto con el fin de descargar los documentos desde el admin
class ModelAnteproyectoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_anteproyecto',
        'nombre_integrante1',
        'nombre_integrante2',
        'director',
        'coodirector',
        'carta_presentacion_link',
        'anteproyecto_link'
    )

    def carta_presentacion_link(self, obj):
        if obj.carta_presentacion:
            if isinstance(obj.carta_presentacion, bytes):  # Asegúrate de que es de tipo bytes
                base64_data = base64.b64encode(obj.carta_presentacion).decode('utf-8')
                url = f'data:application/octet-stream;base64,{base64_data}'
                return format_html(
                    '<a href="{url}" download="{filename}">Descargar Carta de Presentación</a>',
                    url=url,
                    filename='carta_presentacion.pdf'
                )
        return "No cargado"
    carta_presentacion_link.short_description = 'Carta de Presentación'

    def anteproyecto_link(self, obj):
        if obj.anteproyecto:
            if isinstance(obj.anteproyecto, bytes):  # Asegúrate de que es de tipo bytes
                base64_data = base64.b64encode(obj.anteproyecto).decode('utf-8')
                url = f'data:application/octet-stream;base64,{base64_data}'
                return format_html(
                    '<a href="{url}" download="{filename}">Descargar Anteproyecto</a>',
                    url=url,
                    filename='anteproyecto.pdf'
                )
        return "No cargado"
    anteproyecto_link.short_description = 'Anteproyecto'


admin.site.register(ModelAnteproyecto, ModelAnteproyectoAdmin)
