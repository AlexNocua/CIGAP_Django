from django.urls import path
from . import views

# Definicion de las rutas de la aplicacion
urlpatterns = [
    # verificacion del funcionamiento de las rutas de las aplicaciones
    path('', views.funcionando, name='funcionando')
]
