from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required
from login.models import Usuarios
from django.contrib.auth import login as auth_login
import base64
from django.contrib import messages
from django.db.models import Q

# importacion de las funcionalidaes
from plataform_CIGAP.utils.decoradores import grupo_usuario
from plataform_CIGAP.utils.funcionalidades_fechas import fecha_actual, fecha_maxima_respuesta

# importacion de la vista del login que permite cambiar la informacion de ususario
from login.views import editar_usuario
from login.forms import FormEditarUsuario
# Create your views here.

# formulario de retroalimentaciones de correspondencia
from correspondencia.forms import FormObservacionAnteproyecto, FormObservacionProyecto
from correspondencia.views import recuperar_anteproyecto

# importacion de los modelos
from .models import ModelEvaluacionAnteproyecto, ModelEvaluacionProyectoFinal

# importacion de modelos de los estudinates
from estudiante.models import ModelAnteproyecto, ModelProyectoFinal

# impotacion de recuperaciones
from plataform_CIGAP.utils.recuperaciones import recuperar_formatos, datosusuario

# datos del usuario


@login_required
def datos_usuario_director(request):
    usuario = request.user
    imagen = usuario.imagen
    imagen_convertida = base64.b64encode(
        imagen).decode('utf-8') if imagen else ''
    form_editar_usuario = FormEditarUsuario(instance=usuario)

    context = {'form_config': form_editar_usuario, 'usuario': usuario,
               'user_img': imagen_convertida, }
    return context

#############################################################################################################
# utilidades


def recuperar_proyectos_evaluador(request):
    usuario = request.user
    nombre_usuario = usuario.nombre_completo
    proyectos = ModelProyectoFinal.objects.filter(
        Q(anteproyecto__director=nombre_usuario) |
        Q(anteproyecto__codirector=nombre_usuario)
    )
    if not proyectos:
        return None
    return proyectos


def recuperar_evaluacion_anteproyecto(anteproyecto, request):
    usuario = request.user
    evaluacion = ModelEvaluacionAnteproyecto.objects.get(
        Q(anteproyecto=anteproyecto) & Q(evaluador=usuario))
    if not evaluacion:
        return None
    return evaluacion


def recuperar_documento(documento):
    documento = base64.b64encode(documento).decode(
        'utf-8') if documento else None
    return documento


def recuperar_anteproyectos_a_evaluar(request):
    usuario = request.user
    ante_a_evaluar = ModelEvaluacionAnteproyecto.objects.filter(
        Q(evaluador=usuario) & Q(anteproyecto__estado=False))
    if not ante_a_evaluar:
        return None
    return ante_a_evaluar


def recuperar_anteproyectos(request):
    usuario = request.user
    anteproyectos = ModelAnteproyecto.objects.filter(
        (Q(director=usuario.nombre_completo) | Q(
            codirector=usuario.nombre_completo)) & Q(estado=False)
    )
    if not anteproyectos.exists():
        anteproyectos = None

    return anteproyectos


def recuperar_anteproyecto(id):
    anteproyecto = ModelAnteproyecto.objects.get(
        id=id)if ModelAnteproyecto.objects.filter(id=id).exists() else None
    return anteproyecto


def recuperar_proyectos(request):
    usuario = request.user
    proyectos = ModelProyectoFinal.objects.filter((Q(anteproyecto__director=usuario.nombre_completo) | Q(
        anteproyecto__codirector=usuario.nombre_completo)) & Q(estado=False))
    print(proyectos)
    if not proyectos:
        return None
    return proyectos


def recuperar_proyecto(id):
    proyecto = ModelProyectoFinal.objects.get(
        id=id)if ModelProyectoFinal.objects.filter(id=id).exists() else None
    if not proyecto:
        return None
    return proyecto
#############################################################################################################


@login_required
@grupo_usuario('Directores')
def principal_director(request):
    usuario = request.user
    # recuperacion de la imagen propia del usuaario en formato binario
    # print(imagen, 'esta es la imagen')
    imagen = usuario.imagen
    imagen_convertida = base64.b64encode(
        imagen).decode('utf-8') if imagen else ''

    if request.method == 'POST':
        editar_usuario(request)
    else:
        form = FormEditarUsuario(instance=usuario)
        return render(request, 'director/base_director.html', {'form_config': form, 'usuario': usuario, 'user_img': imagen_convertida})

# def base_director(request):
#     usuario = request.user
#     # recuperacion de la imagen propia del usuaario en formato binario
#     # print(imagen, 'esta es la imagen')
#     imagen = usuario.imagen
#     imagen_convertida = base64.b64encode(imagen).decode('utf-8') if imagen else ''

#     if request.method == 'POST':
#         form = FormEditarUsuario(request.POST, request.FILES, instance=usuario)
#         if form.is_valid():
#             user = form.save()


def view_anteproyectos(request):
    context = datos_usuario_director(request)
    anteproyectos = recuperar_anteproyectos(request)
    if anteproyectos:
        context['anteproyectos'] = anteproyectos
    return render(request, 'director/anteproyectos/anteproyectos.html', context)


def anteproyecto(request, id):
    context = {}
    # Recuperar el anteproyecto
    anteproyecto = recuperar_anteproyecto(id)
    context['anteproyecto'] = anteproyecto
    if anteproyecto:
        if anteproyecto.fecha_envio:
            context['fecha_respuesta_maxima'] = fecha_maxima_respuesta(
                anteproyecto.fecha_envio)
        doc_anteproyecto = recuperar_documento(anteproyecto.anteproyecto)
        doc_carta_presentacion = recuperar_documento(
            anteproyecto.carta_presentacion)
        context['doc_anteproyecto'] = doc_anteproyecto
        context['doc_carta_presentacion'] = doc_carta_presentacion

    if request.method == 'POST':
        formulario_observacion = FormObservacionAnteproyecto(
            request.POST, request.FILES)

        if formulario_observacion.is_valid():

            retroalimentacion = formulario_observacion.save(commit=False)
            retroalimentacion.user = request.user
            retroalimentacion.anteproyecto = anteproyecto
            retroalimentacion.fecha_retroalimentacion = fecha_actual()

            retroalimentacion.save()

            messages.success(
                request, 'La retroalimentación se envió correctamente.')

        else:
            messages.error(
                request, f'Hubo un error al enviar la retroalimentación. Por favor, revise los campos. {formulario_retroalimentacion.errors}')

    else:
        formulario_retroalimentacion = FormObservacionAnteproyecto()
        context['from_retroalimentacion'] = formulario_retroalimentacion
    return render(request, 'director/anteproyectos/anteproyecto.html', context)


def enviar_anteproyecto(request, id):
    anteproyecto = recuperar_anteproyecto(id)
    if anteproyecto.solicitud_enviada == True:
        messages.error(
            request, f'El anteproyecto "{anteproyecto.nombre_anteproyecto}" ya fue enviado al comité el {anteproyecto.fecha_envio}. Por favor, esté atento a posibles respuestas.')
        return redirect('director:anteproyecto', id=id)
    if anteproyecto:
        anteproyecto.solicitud_enviada = True
        anteproyecto.fecha_envio = fecha_actual()
        anteproyecto.save()
        messages.success(
            request, f'El anteproyecto "{anteproyecto.nombre_anteproyecto}" ha sido enviado al comité. Por favor, esté atento a posibles respuestas.')
        return redirect('director:anteproyecto', id=id)
    else:
        messages.error(
            request, 'No se pudo encontrar el anteproyecto especificado.')
        return redirect('director:anteproyecto', id=id)

#############################################################################################################


#############################################################################################################
# configuracion de las vistas del modulo de proyectos


def view_proyectos(request):
    context = datos_usuario_director(request)
    proyectos = recuperar_proyectos(request)
    if proyectos:
        context['proyectos'] = proyectos

    return render(request, 'director/proyectos/proyectos.html', context)


def proyecto(request, id):
    context = {}
    proyecto = recuperar_proyecto(id)
    if proyecto:
        context['proyecto_final'] = proyecto
        doc_proyecto_final = recuperar_documento(proyecto.proyecto_final)
        doc_carta_presentacion_final = recuperar_documento(
            proyecto.carta_presentacion_final)
        context['doc_proyecto_final'] = doc_proyecto_final
        context['doc_carta_presentacion_final'] = doc_carta_presentacion_final

    if request.method == 'POST':
        formulario_observacion = FormObservacionProyecto(
            request.POST, request.FILES)

        if formulario_observacion.is_valid():

            retroalimentacion = formulario_observacion.save(commit=False)
            retroalimentacion.proyecto_final = proyecto
            retroalimentacion.save()

            messages.success(
                request, 'La retroalimentación se envió correctamente.')

        else:
            messages.error(
                request, f'Hubo un error al enviar la retroalimentación. Por favor, revise los campos. {formulario_retroalimentacion.errors}')
    else:
        formulario_observacion = FormObservacionProyecto()
        context['from_retroalimentacion'] = formulario_observacion
    return render(request, 'director/proyectos/proyecto.html', context)


def enviar_proyecto(request, id):
    proyecto = recuperar_proyecto(id)
    if proyecto.solicitud_enviada == True:
        messages.error(
            request, f'El proyecto "{proyecto.anteproyecto.nombre_anteproyecto}" ya fue enviado al comité el {proyecto.fecha_envio}. Por favor, esté atento a posibles respuestas.')
        return redirect('director:proyecto', id=id)
    if proyecto:
        proyecto.solicitud_enviada = True
        proyecto.fecha_envio = fecha_actual()
        proyecto.save()
        messages.success(
            request, f'El proyecto "{proyecto.anteproyecto.nombre_anteproyecto}" ha sido enviado al comité. Por favor, esté atento a posibles respuestas.')
        return redirect('director:proyecto', id=id)
    else:
        messages.error(
            request, 'No se pudo encontrar el proyecto especificado.')
        return redirect('director:proyecto', id=id)
#############################################################################################################


#############################################################################################################
# configuracion de las vistas del modulo de anteproyecto


def evaluacion_proyectos(request):
    context = datos_usuario_director(request)

    return render(request, 'director/evaluacion_proyectos/eva_proyectos.html', context)


def view_evaluador_anteproyectos(request):
    context = datos_usuario_director(request)
    anteproyectos = recuperar_anteproyectos_a_evaluar(request)
    if anteproyectos:
        context['anteproyectos'] = anteproyectos
    return render(request, 'director/evaluacion_proyectos/list_evaluador.html', context)


def evaluar_anteproyecto(request, id):
    context = datos_usuario_director(request)
    anteproyecto = recuperar_anteproyecto(id)
    if anteproyecto:
        evaluacion = recuperar_evaluacion_anteproyecto(anteproyecto, request)
        if evaluacion:
            documento_evaluacion = recuperar_documento(
                evaluacion.doc_evaluacion_anteproyecto)
            print(documento_evaluacion, 'documento')
            context['doc_evaluacion_anteproyecto'] = documento_evaluacion
            context['evaluacion'] = evaluacion
        context['anteproyecto'] = anteproyecto
        doc_anteproyecto = recuperar_documento(anteproyecto.anteproyecto)
        context['doc_anteproyecto'] = doc_anteproyecto
    return render(request, 'director/evaluacion_proyectos/anteproyecto.html', context)


def enviar_evaluacion(request, id):
    context = datos_usuario_director(request)
    anteproyecto = recuperar_anteproyecto(id)
    if anteproyecto:
        evaluacion_anteproyecto = recuperar_evaluacion_anteproyecto(
            anteproyecto, request)
        if evaluacion_anteproyecto:

            evaluacion_anteproyecto.calificacion = request.POST.get(
                'calificacion')
            evaluacion_anteproyecto.comentarios = request.POST.get(
                'comentarios')
            evaluacion_anteproyecto.estado = request.POST.get(
                'estado') == 'True'
            doc_retro = request.FILES.get(
                'doc_retroalimentacion_convert')

            if doc_retro:
                evaluacion_anteproyecto.doc_evaluacion_anteproyecto = doc_retro.read()

            evaluacion_anteproyecto.fecha_evaluacion = fecha_actual()
            evaluacion_anteproyecto.save()

            messages.success(
                request, f'La evaluación del anteproyecto "{anteproyecto.nombre_anteproyecto}" ha sido guardada con la calificación {evaluacion_anteproyecto.calificacion}.')

            return redirect('director:evaluar_anteproyecto', id=id)

        else:
            messages.error(
                request, f'No se encontró la evaluación para el anteproyecto "{anteproyecto.nombre_anteproyecto}".')

    else:
        messages.error(request, f'El anteproyecto con ID {id} no existe.')

    return redirect('director:evaluar_anteproyecto', id=id)


def view_jurado(request):
    context = datos_usuario_director(request)
    proyectos = recuperar_proyectos_evaluador(request)
    if proyectos:
        context['proyectos'] = proyectos
        print(proyectos)
    return render(request, 'director/evaluacion_proyectos/list_jurado.html', context)
#############################################################################################################
# formatos de correspondencia


def formatos_documentos(request):
    context = datosusuario(request)
    context['formatos'] = recuperar_formatos()

    return render(request, 'director/formatos/formatos.html', context)
