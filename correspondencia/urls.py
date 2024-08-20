from django.urls import path
from . import views

# importante la asiganicion de APPNAME para el reverso de funciones utilizando URLs
app_name = 'correspondencia'

# Definicion de las rutas de la aplicacion
urlpatterns = [
    # verificacion del funcionamiento de las rutas de las aplicaciones
    path('', views.funcionando, name='funcionando')
]
