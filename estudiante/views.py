
# get_object_or_404 para el manejo de errores si no se encuentra un modelo con los siguientes datos
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponsePermanentRedirect

from django.contrib.auth.decorators import login_required
from plataform_CIGAP.decoradores import grupo_usuario

# formulario de anteproyecto
from .forms import FormAnteproyecto


# modelos
from .models import ModelAnteproyecto
import base64

# importacion de la vista del login que permite cambiar la informacion de ususario
from login.views import editar_usuario
# importacion del formulario para editar el usuario
from login.forms import FormEditarUsuario

# Create your views here.

# vista de funcionamiento respecto a la url de la aplicacion
# def funcionando(request):
#     return HttpResponse('app_ estudiante funcionando.')


@login_required
@grupo_usuario('Estudiantes')
def datosusuario(request):
    usuario = request.user
    imagen = usuario.imagen
    imagen_convertida = base64.b64encode(
        imagen).decode('utf-8') if imagen else ''
    form_editar_usuario = FormEditarUsuario(instance=usuario)
    form_solicitud = FormAnteproyecto
    context = {'form_anteproyecto': form_solicitud,
               'form_config': form_editar_usuario, 'usuario': usuario, 'user_img': imagen_convertida
               }
    return context


# funcion para devolver un diccionario con los datos del proyecto
def contenido_anteproyecto(request):
    content_anteproyecto = get_object_or_404(
        ModelAnteproyecto, user=request.user)
    context = {
        'nombre_proyecto': content_anteproyecto.nombre_proyecto,
        'integrante1': content_anteproyecto.nombre_integrante1,
        'integrante2': content_anteproyecto.nombre_integrante2,
        'director': content_anteproyecto.director,
        'codirector': content_anteproyecto.coodirector,
        'retroalimentacion': content_anteproyecto.estado_solicitud_anteproyecto,
        'estado': content_anteproyecto.estado_solicitud_anteproyecto,
        'rev_dadas': content_anteproyecto.rev_dadas,
    }
    # print(context)
    return context


@login_required
@grupo_usuario('Estudiantes')
def principal_estudiante(request):

    if request.method == 'POST':
        editar_usuario(request)
    else:
        context = datosusuario(request)
        return render(request, 'estudiante/base_estudiante.html', context)

# vista del template para la solicitud


#!funcionando
@login_required
@grupo_usuario('Estudiantes')
def solicitud(request):
    if request.method == 'POST':
        form = FormAnteproyecto(request.POST, request.FILES)
        if form.is_valid():
            # Crea una instancia del modelo sin guardarla en la base de datos aún
            anteproyecto = form.save(commit=False)
            anteproyecto.user = request.user  # Asigna el usuario actual al campo user
            anteproyecto.save()  # Guarda la instancia del modelo en la base de datos
            return redirect('estudiante:solicitud')
        else:
            return HttpResponse('Algo pasó', form.errors)
    else:
        context = datosusuario(request)
        return render(request, 'estudiante/solicitud.html', context)
# vista de la informacion del proyecto


def info_proyect(request):
    if request.method == 'POST':
        context = contenido_anteproyecto(request)
        return render(request, 'estudiante/Inf_proyect.html',context)
        
    else:
        contenido_anteproyecto(request)
        return render(request, 'estudiante/Inf_proyect.html')
