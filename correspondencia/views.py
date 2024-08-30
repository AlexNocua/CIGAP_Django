import django.contrib.auth
from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from plataform_CIGAP.views import logout_user
from django.contrib.auth.decorators import login_required
import base64
# importacion de las funcionalidaes
from plataform_CIGAP.utils.decoradores import grupo_usuario
from plataform_CIGAP.utils.funcionalidades_fechas import fecha_actual

# importacion de los modelos
from estudiante.models import ModelAnteproyecto
from login.models import Usuarios
from nombres import nombre_completo

# Create your views here.
# def funcionando (request):
#     return HttpResponse('app_ correspondencia funcionando.')


# funcion para traer los anteproyectos
def recuperar_anteproyectos():
    anteproyectos = ModelAnteproyecto.objects.all()
    return anteproyectos

# funcion para traer un anteproyecto en especifico


def recuperar_anteproyecto(nombre):
    anteproyecto = ModelAnteproyecto.objects.get(
        nombre_proyecto=nombre) if ModelAnteproyecto.objects.filter(nombre_proyecto=nombre).exists() else False
    return anteproyecto

# funcion para recuperar las imagenes de los estudiantes


def recuperar_datos_integrantes(nombre):
    usuario = Usuarios.objects.get(nombre_completo=nombre) if Usuarios.objects.filter(
        nombre_completo=nombre).exists() else False
    if usuario:
        imagen_binaria = usuario.imagen
        imagen = base64.b64encode(imagen_binaria).decode(
            'utf8') if imagen_binaria else False
        return {'nombre': nombre, 'imagen': imagen}
    else:
        return {'nombre': nombre}


@login_required
@grupo_usuario('Correspondencia')
def principal_correspondencia(request):
    return render(request, 'correspondencia/base_correspondencia.html')


@login_required
@grupo_usuario('Correspondencia')
def view_list_proyects(request):
    anteproyectos = recuperar_anteproyectos()
    context = {'anteproyectos': anteproyectos}
    return render(request, 'correspondencia/list_proyectos.html', context)

# vista para conocer la informacion del proyecto


def ver_anteproyecto(request, nombre_anteproyecto):
    anteproyecto = recuperar_anteproyecto(nombre_anteproyecto)
    if anteproyecto:
        integrantes = (anteproyecto.nombre_integrante1, anteproyecto.nombre_integrante2)
        datos_integrantes = {    }
        for i,integrante in enumerate(integrantes):
            if integrante:
                datos_integrantes[f'integrante_{i}'] = recuperar_datos_integrantes(integrante)
        return render(request, 'correspondencia/anteproyecto.html', datos_integrantes)
    else:
        return HttpResponse(f'Gestiona los poryectos existentes, algo paso con este.')
    # return HttpResponse(f'Nombre del anteproyecto: {nombre_anteproyecto}')
