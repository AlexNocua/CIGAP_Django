from django.urls import path
from . import views

# importante la asiganicion de APPNAME para el reverso de funciones utilizando URLs
app_name = 'correspondencia'

# Definicion de las rutas de la aplicacion
urlpatterns = [
    # verificacion del funcionamiento de las rutas de las aplicaciones
    # path('', views.funcionando, name='funcionando')
    path('', views.principal_correspondencia,
         name='principal_correspondencia'),
    ###################################################################################################
    path('solicitudes', views.solicitudes, name='solicitudes'),
    path('solicitudes_anteproyectos', views.solicitudes_anteproyectos,
         name='solicitudes_anteproyectos'),
    path('asignar_evaluadores_ante/<int:id>', views.asignar_evaluadores_ante,
         name='asignar_evaluadores_ante'),
    path('solicitudes_proyectos_finales', views.solicitudes_proyectos_finales,
         name='solicitudes_proyectos_finales'),
    path('solicitudes_especiales', views.solicitudes_especiales,
         name='solicitudes_especiales'),
    path('actualizar_datos_solicitud_anteproyecto/<int:id>',
         views.actualizar_datos_solicitud_anteproyecto, name='actualizar_datos_solicitud_anteproyecto'),
    path('actualizar_datos_solicitud_proyecto/<int:id>',
         views.actualizar_datos_solicitud_proyecto, name='actualizar_datos_solicitud_proyecto'),
    path('enviar_retroalimentacion_solicitud/<int:id>',
         views.enviar_retroalimentacion_solicitud, name='enviar_retroalimentacion_solicitud'),
    ###################################################################################################
    path('solicitudes_respondidas', views.solicitudes_respondidas,
         name='solicitudes_respondidas'),
    path('view_solicitud_especial/<int:id>', views.view_solicitud_especial,
         name='view_solicitud_especial'),
    path('ver_respuesta/<int:id>', views.ver_respuesta,
         name='ver_respuesta'),
    #     path('documentos_cargados', views.documentos_cargados,
    #          name='documentos_cargados'),
    ##############################################################################################
    path('formatos_documentos', views.formatos_documentos,
         name='formatos_documentos'),
    path('editar_formato/<int:id>', views.editar_formato,
         name='editar_formato'),
    path('eliminar_formato/<int:id>', views.eliminar_formato,
         name='eliminar_formato'),
    ##############################################################################################
    path('ver_anteproyecto/<str:nombre_anteproyecto>',
         views.ver_anteproyecto, name='ver_anteproyecto'),
    path('ver_proyecto_final/<str:nombre>/',
         views.ver_proyecto_final, name='ver_proyecto_final'),
    path('enviar_retroalimentacion/<str:nombre_anteproyecto>',
         views.enviar_retroalimentacion, name='enviar_retroalimentacion'),
    path('asignar_jurados/<str:nombre>',
         views.asignar_jurados, name='asignar_jurados'),
    ##############################################################################################
    path('proyectos',
         views.proyectos, name='proyectos'),
    path('proyectos_finalizados',
         views.proyectos_finalizados, name='proyectos_finalizados'),
    path('proyectos_actuales',
         views.proyectos_actuales, name='proyectos_actuales'),
    path('proyecto_final/<int:id>',
         views.proyecto_final, name='proyecto_final'),
    path('proyecto_actual/<int:id>',
         views.proyecto_actual, name='proyecto_actual'),



]
