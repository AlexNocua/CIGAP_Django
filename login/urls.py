from . import views


from django.contrib import admin
from django.urls import path, include
app_name = 'login'


urlpatterns = [
    #  ruta de registro para el patterns de la app
    path('', views.loginapps, name='loginapps'),
    path('registro', views.registro, name='registro'),
]
