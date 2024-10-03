import base64
from .models import ModelAnteproyecto
from django.contrib import admin

# Para conseguir renderizar componentes en el admin
from django.utils.html import format_html

from .models import ModelAnteproyecto, ModelProyectoFinal, ModelObjetivoGeneral, ModelObjetivosEspecificos, ModelActividades, ModelFechasProyecto, ModelAsignacionJurados
# Register your models here.
# Revisar esto con el fin de descargar los documentos desde el admin


class ModelAnteproyectoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_anteproyecto',
        'nombre_integrante1',
        'nombre_integrante2',
        'director',
        'codirector',
        'carta_presentacion_link',
        'anteproyecto_link'

    )

    def carta_presentacion_link(self, obj):
        if obj.carta_presentacion:
            if isinstance(obj.carta_presentacion, bytes):  # Asegúrate de que es de tipo bytes
                base64_data = base64.b64encode(
                    obj.carta_presentacion).decode('utf-8')
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
                base64_data = base64.b64encode(
                    obj.anteproyecto).decode('utf-8')
                url = f'data:application/octet-stream;base64,{base64_data}'
                return format_html(
                    '<a href="{url}" download="{filename}">Descargar Anteproyecto</a>',
                    url=url,
                    filename='anteproyecto.pdf'
                )
        return "No cargado"
    anteproyecto_link.short_description = 'Anteproyecto'


admin.site.register(ModelAnteproyecto, ModelAnteproyectoAdmin)


class ModelProyectoFinalAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'anteproyecto',
        'fecha_envio',
        'solicitud_enviada',
        'estado',
        'carta_presentacion_final_link',
        'proyecto_final_link'
    )

    def carta_presentacion_final_link(self, obj):
        if obj.carta_presentacion_final:
            # Asegúrate de que es de tipo bytes
            if isinstance(obj.carta_presentacion_final, bytes):
                base64_data = base64.b64encode(
                    obj.carta_presentacion_final).decode('utf-8')
                url = f'data:application/octet-stream;base64,{base64_data}'
                return format_html(
                    '<a href="{url}" download="carta_presentacion_final.pdf">Descargar Carta de Presentación Final</a>',
                    url=url
                )
        return "No cargado"
    carta_presentacion_final_link.short_description = 'Carta de Presentación Final'

    def proyecto_final_link(self, obj):
        if obj.proyecto_final:
            if isinstance(obj.proyecto_final, bytes):
                base64_data = base64.b64encode(
                    obj.proyecto_final).decode('utf-8')
                url = f'data:application/octet-stream;base64,{base64_data}'
                return format_html(
                    '<a href="{url}" download="proyecto_final.pdf">Descargar Proyecto Final</a>',
                    url=url
                )
        return "No cargado"
    proyecto_final_link.short_description = 'Proyecto Final'


admin.site.register(ModelProyectoFinal, ModelProyectoFinalAdmin)


###########################################################################
# tener en cuenta estas nuevas formas de registro de los modelos en el panel de administracion


@admin.register(ModelObjetivoGeneral)
class ModelObjetivoGeneralAdmin(admin.ModelAdmin):
    list_display = ('proyecto_final', 'descripcion', )
    search_fields = ('descripcion',)


@admin.register(ModelObjetivosEspecificos)
class ModelObjetivosEspecificosAdmin(admin.ModelAdmin):
    list_display = ('objetivo_general', 'descripcion', 'estado')
    search_fields = ('descripcion',)
    list_filter = ('estado',)


@admin.register(ModelActividades)
class ModelActividadesAdmin(admin.ModelAdmin):
    list_display = ('objetivo_general', 'objetivos_especificos',
                    'descripcion', 'estado')
    search_fields = ('descripcion',)
    list_filter = ('estado',)


# creacion personalizada en el admin de django.


class ModelFechasProyectoAdmin(admin.ModelAdmin):
    list_display = ('proyecto_final', 'fecha_inicio', 'fecha_finalizacion', 'fecha_etapa_uno', 'fecha_etapa_dos',
                    'fecha_etapa_tres', 'fecha_etapa_cuatro', 'fecha_etapa_cinco', 'fecha_etapa_seis')
    search_fields = ('proyecto__nombre',)
    list_filter = ('fecha_inicio', 'fecha_finalizacion')


admin.site.register(ModelFechasProyecto, ModelFechasProyectoAdmin)


# class ModelAsignacionJuradosAdmin(admin.ModelAdmin):
#     list_display = ('proyecto_final', 'nombre_jurado', 'fecha_sustentacion')
#     search_fields = ('nombre_jurado', 'proyecto_final__nombre_anteproyecto')
#     list_filter = ('fecha_sustentacion',)
#     date_hierarchy = 'fecha_sustentacion'

#     def get_queryset(self, request):
#         # Esto asegura que los jurados se obtengan de manera eficiente con el proyecto final relacionado
#         queryset = super().get_queryset(request)
#         return queryset.select_related('proyecto_final')


# admin.site.register(ModelAsignacionJurados, ModelAsignacionJuradosAdmin)
