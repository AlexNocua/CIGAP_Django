from django.urls import path
from . import views

# importante la asiganicion de APPNAME para el reverso de funciones utilizando URLs
app_name = 'estudiante'


# Definicion de las rutas de la aplicacion
urlpatterns = [
    # verificacion del funcionamiento de las rutas de las aplicaciones
    # path('', views.funcionando, name='funcionando'),
    path('', views.principal_estudiante, name='principal_estudiante'),
    # path('estudiante', views.estudiante, name='estudiante'),
    #!funcionando
    path('solicitud', views.solicitud, name='solicitud'),
]