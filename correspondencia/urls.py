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
    path('view_list_proyects', views.view_list_proyects, name='view_list_proyects'),
    path('ver_proyecto/<str:nombre_anteproyecto>',
         views.ver_anteproyecto, name='ver_anteproyecto'),

]
