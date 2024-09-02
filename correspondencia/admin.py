from django.contrib import admin
from django.utils.html import format_html
from .models import ModelRetroalimentacionesAnteproyecto
import base64
# Register your models here.


class ModelRetroalimentacionesAnteproyectoAdmin(admin.ModelAdmin):
    list_display = ('anteproyecto', 'retroalimentacion', 'fecha_retroalimentacion', 'estado', 'revs_dadas', 'doc_retroalimentacion_link')

    def doc_retroalimentacion_link(self, obj):
        if obj.doc_retroalimentacion:
            if isinstance(obj.doc_retroalimentacion, bytes):
                base64_data = base64.b64encode(obj.doc_retroalimentacion).decode('utf8')
                url = f'data:application/octet-stream;base64,{base64_data}'
                return format_html('<a href="{}" download="{}">Descargar Carta de Presentación</a>',
                                   url,
                                   f'Retroalimentacion_{obj.anteproyecto.nombre_anteproyecto}.pdf')
        return 'No Cargado'
    doc_retroalimentacion_link.short_description = 'Documento retroalimentado'

admin.site.register(ModelRetroalimentacionesAnteproyecto,
                    ModelRetroalimentacionesAnteproyectoAdmin)
