from django.contrib import admin
from django.utils.html import format_html
from .models import ModelRetroalimentaciones, ModelAsignacionJurados, ModelInformacionEntregaFinal, ModelSolicitudes,ModelDocumentos
import base64
# Register your models here.

# Registro del modelo de retroalimentaciones en el panel admin


class ModelRetroalimentacionesAdmin(admin.ModelAdmin):
    list_display = ('anteproyecto', 'proyecto_final', 'retroalimentacion', 'fecha_retroalimentacion',
                    'estado', 'revs_dadas', 'doc_retroalimentacion_link')

    def doc_retroalimentacion_link(self, obj):
        if obj.doc_retroalimentacion:
            if isinstance(obj.doc_retroalimentacion, bytes):
                base64_data = base64.b64encode(
                    obj.doc_retroalimentacion).decode('utf8')
                url = f'data:application/octet-stream;base64,{base64_data}'
                if obj.anteproyecto:
                    nombre_anteproyecto = obj.anteproyecto.nombre_anteproyecto
                else:
                    nombre_anteproyecto = 'Desconocido'
                return format_html('<a href="{}" download="{}">Descargar Carta de Presentación</a>',
                                   url,
                                   f'Retroalimentacion_{nombre_anteproyecto}.pdf')
        return 'No Cargado'
    doc_retroalimentacion_link.short_description = 'Documento retroalimentado'


admin.site.register(ModelRetroalimentaciones,
                    ModelRetroalimentacionesAdmin)

# Registro del modelo de Asignacion de jurados en el panel admin
admin.site.register(ModelAsignacionJurados)
# Registro del modelo de Informacion de entrega Final de jurados en el panel admin
admin.site.register(ModelInformacionEntregaFinal)
# registro del modelo de solicitudes especificas
admin.site.register(ModelSolicitudes) 
# registro del modele de formatos
admin.site.register(ModelDocumentos) 
