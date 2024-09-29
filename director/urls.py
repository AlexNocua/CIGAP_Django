from django.urls import path
from . import views


# importante la asiganicion de APPNAME para el reverso de funciones utilizando URLs
app_name = 'director'


# Definicion de las rutas de la aplicacion
urlpatterns = [
    # verificacion del funcionamiento de las rutas de las aplicaciones
    # path('', views.funcionando, name='funcionando'),
    path('', views.principal_director, name='principal_director'),
    ########################################################################
    # vinculos del modulo de anteproyecto
    path('view_anteproyectos', views.view_anteproyectos, name='view_anteproyectos'),
    path('anteproyecto/<int:id>', views.anteproyecto, name='anteproyecto'),
    path('enviar_anteproyecto/<int:id>', views.enviar_anteproyecto, name='enviar_anteproyecto'),
    ########################################################################
    # vinculos del modulo de proyectos
    path('view_proyectos', views.view_proyectos, name='view_proyectos'),
    path('proyecto/<int:id>', views.proyecto, name='proyecto'),
    path('enviar_proyecto/<int:id>', views.enviar_proyecto, name='enviar_proyecto'),
    ########################################################################
    # vinculos del modulo de evaluacion de proyectos
    path('evaluacion_proyectos', views.evaluacion_proyectos, name='evaluacion_proyectos'),
    path('view_evaluador', views.view_evaluador, name='view_evaluador'),
    path('view_jurado', views.view_jurado, name='view_jurado'),
    ########################################################################
]
