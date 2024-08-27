
# get_object_or_404 para el manejo de errores si no se encuentra un modelo con los siguientes datos
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponsePermanentRedirect

from django.contrib.auth.decorators import login_required
# formulario de anteproyecto

from .forms import FormAnteproyecto
# modelos
from .models import ModelAnteproyecto
import base64
# importacion de la vista del login que permite cambiar la informacion de ususario
from login.views import editar_usuario
# importacion del formulario para editar el usuario
from login.forms import FormEditarUsuario
# importacion de las funcionalidaes
from plataform_CIGAP.utils.decoradores import grupo_usuario
from plataform_CIGAP.utils.funcionalidades_fechas import fecha_actual


# Create your views here.

# vista de funcionamiento respecto a la url de la aplicacion
# def funcionando(request):
#     return HttpResponse('app_ estudiante funcionando.')


# funcion para devolver documentos o imagenes
def devolver_documento_imagen(documento_binario):
    documento = base64.b64encode(documento_binario).decode(
        'utf-8') if documento_binario else ''
    return documento


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
    try:

        content_anteproyecto = get_object_or_404(ModelAnteproyecto, user=request.user)
        carta_presentacion_binario = content_anteproyecto.carta_presentacion
        anteproyecto_binario = content_anteproyecto.anteproyecto
        carta_presentacion = devolver_documento_imagen(
            carta_presentacion_binario)
        anteproyecto = devolver_documento_imagen(anteproyecto_binario)
        context_anteproyecto = {
            'nombre_proyecto': content_anteproyecto.nombre_proyecto,
            'integrante1': content_anteproyecto.nombre_integrante1,
            'integrante2': content_anteproyecto.nombre_integrante2,
            'director': content_anteproyecto.director,
            'carta': carta_presentacion,
            'anteproyecto': anteproyecto,
            'codirector': content_anteproyecto.coodirector,
            'retroalimentacion': content_anteproyecto.estado_solicitud_anteproyecto,
            'estado': content_anteproyecto.estado_solicitud_anteproyecto,
            'rev_dadas': content_anteproyecto.rev_dadas,
            'retroalimentacion': content_anteproyecto.retroalimentacion,
            'existe_solicitud': True,
           
        }
       
    except:
        context_anteproyecto = {
            'existe_solicitud': False,
        }
        # print(context)
    return context_anteproyecto


@ login_required
@ grupo_usuario('Estudiantes')
def principal_estudiante(request):

    if request.method == 'POST':
        editar_usuario(request)
    else:
        context = datosusuario(request)
        return render(request, 'estudiante/base_estudiante.html', context)

# vista del template para la solicitud


#!funcionando
@ login_required
@ grupo_usuario('Estudiantes')
def solicitud(request):
    if request.method == 'POST':
        form = FormAnteproyecto(request.POST, request.FILES)
        if form.is_valid():
            # Crea una instancia del modelo sin guardarla en la base de datos aún
            anteproyecto = form.save(commit=False)
            anteproyecto.fecha_envio = fecha_actual
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
        return render(request, 'estudiante/Inf_proyect.html', context)
    else:
        context = contenido_anteproyecto(request)
        return render(request, 'estudiante/Inf_proyect.html', context)
