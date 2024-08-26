from django.urls import path
from . import views


# importante la asiganicion de APPNAME para el reverso de funciones utilizando URLs
app_name = 'director'


# Definicion de las rutas de la aplicacion
urlpatterns = [
    # verificacion del funcionamiento de las rutas de las aplicaciones
    # path('', views.funcionando, name='funcionando'),
    path('', views.principal_director, name='principal_director'),
   
]
