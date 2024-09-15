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
    path('solicitudes_proyectos_finales', views.solicitudes_proyectos_finales,
         name='solicitudes_proyectos_finales'),
    path('solicitudes_especiales', views.solicitudes_especiales,
         name='solicitudes_especiales'),
    ###################################################################################################
    path('solicitudes_respondidas', views.solicitudes_respondidas,
         name='solicitudes_respondidas'),
    path('view_solicitud_especial/<int:id>', views.view_solicitud_especial,
         name='view_solicitud_especial'),
    path('ver_respuesta/<int:id>', views.ver_respuesta,
         name='ver_respuesta'),
    path('documentos_cargados', views.documentos_cargados,
         name='documentos_cargados'),
    path('formatos_documentos', views.formatos_documentos,
         name='formatos_documentos'),
    path('ver_anteproyecto/<str:nombre_anteproyecto>',
         views.ver_anteproyecto, name='ver_anteproyecto'),
    path('ver_proyecto_final/<str:nombre>/',
         views.ver_proyecto_final, name='ver_proyecto_final'),
    path('enviar_retroalimentacion/<str:nombre_anteproyecto>',
         views.enviar_retroalimentacion, name='enviar_retroalimentacion'),
    path('asignar_jurados',
         views.asignar_jurados, name='asignar_jurados'),



]
