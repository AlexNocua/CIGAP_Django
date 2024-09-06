
# get_object_or_404 para el manejo de errores si no se encuentra un modelo con los siguientes datos
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.core.exceptions import ObjectDoesNotExist


from django.contrib.auth.decorators import login_required
# formulario de anteproyecto


from .forms import FormAnteproyecto, FormProyectoFinal
# modelos
from .models import ModelAnteproyecto
import base64
# modelo de correspondencia
from correspondencia.models import ModelRetroalimentaciones

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
        'utf-8') if documento_binario else None
    return documento


@login_required
def datosusuario(request):
    anteproyecto = ModelAnteproyecto.objects.get(
        user=request.user) if ModelAnteproyecto.objects.filter(user=request.user).exists() else None
    usuario = request.user
    imagen = usuario.imagen
    imagen_convertida = base64.b64encode(
        imagen).decode('utf-8') if imagen else ''
    form_editar_usuario = FormEditarUsuario(instance=usuario)
    form_solicitud = FormAnteproyecto
    if anteproyecto:
        context = {'form_anteproyecto': form_solicitud, 'form_config': form_editar_usuario, 'usuario': usuario,
                   'user_img': imagen_convertida, 'nombre_anteproyecto': anteproyecto.nombre_anteproyecto, }

    else:
        context = {'form_anteproyecto': form_solicitud, 'form_config': form_editar_usuario, 'usuario': usuario,
                   'user_img': imagen_convertida, 'nombre_anteproyecto': None}
    return context


# funcion para devolver un diccionario con los datos del proyecto
def contenido_anteproyecto(request):
    try:
        content_anteproyecto = ModelAnteproyecto.objects.get(user=request.user)
        carta_presentacion_binario = content_anteproyecto.carta_presentacion
        anteproyecto_binario = content_anteproyecto.anteproyecto
        carta_presentacion = devolver_documento_imagen(
            carta_presentacion_binario)
        anteproyecto = devolver_documento_imagen(anteproyecto_binario)

        context_anteproyecto = {
            'nombre_anteproyecto': content_anteproyecto.nombre_anteproyecto,
            'integrante1': content_anteproyecto.nombre_integrante1,
            'integrante2': content_anteproyecto.nombre_integrante2,
            'director': content_anteproyecto.director,
            'descripcion': content_anteproyecto.descripcion,
            'carta': carta_presentacion,
            'fecha_envio': content_anteproyecto.fecha_envio,
            'anteproyecto': anteproyecto,
            'solicitud_enviada': content_anteproyecto.solicitud_enviada,
            'codirector': content_anteproyecto.codirector,

        }

    except ObjectDoesNotExist:
        context_anteproyecto = {
            'solicitud_enviada': False,
        }
    except Exception as e:
        print(f'Error: {e}')
        context_anteproyecto = {
            'solicitud_enviada': False,
        }

    return context_anteproyecto


# funcion para recuperar las retroalimentaciones de correspondencia
def recuperar_retroalimentacion(anteproyecto_):
    retroalimentaciones = ModelRetroalimentaciones.objects.get(
        anteproyecto=anteproyecto_) if ModelRetroalimentaciones.objects.filter(anteproyecto=anteproyecto_).exists() else None
    doc_convert = devolver_documento_imagen(
        retroalimentaciones.doc_retroalimentacion)
    return {'respuesta': retroalimentaciones,
            'doc_retroalimentacion': doc_convert}


def recuperar_anteproyecto(request):
    anteproyecto = ModelAnteproyecto.objects.get(
        user=request.user) if ModelAnteproyecto.objects.filter(user=request.user).exists() else None
    return anteproyecto


@ login_required
@ grupo_usuario('Estudiantes')
def principal_estudiante(request):
    context = {}
    anteproyecto = recuperar_anteproyecto(request)
    retroalimentacion = recuperar_retroalimentacion(anteproyecto)
    if request.method == 'POST':
        editar_usuario(request)
    else:

        context = datosusuario(request)
        context['retroalimentacion'] = retroalimentacion

        return render(request, 'estudiante/base_estudiante.html', context)

# vista del template para la solicitud


#!funcionando
@ login_required
@ grupo_usuario('Estudiantes')
def solicitud(request):
    context = datosusuario(request)
    # Si el método es POST, procesamos el formulario.
    if request.method == 'POST':
        form = FormAnteproyecto(request.POST, request.FILES)
        if form.is_valid():
            anteproyecto = form.save(commit=False)
            anteproyecto.fecha_envio = fecha_actual()
            anteproyecto.solicitud_enviada = True
            anteproyecto.user = request.user  # Asigna el usuario actual al campo user
            anteproyecto.save()
            return redirect('estudiante:info_proyect')

    # Si el método es GET, buscamos el anteproyecto del usuario actual.
    else:

        try:
            content_anteproyecto = ModelAnteproyecto.objects.get(
                user=request.user)
        except ModelAnteproyecto.DoesNotExist:
            content_anteproyecto = None

        if content_anteproyecto:
            existe_solicitud = content_anteproyecto.solicitud_enviada
            nombre_anteproyecto = content_anteproyecto.nombre_anteproyecto
            form_anteproyecto = FormAnteproyecto(instance=content_anteproyecto)
            context['form_anteproyecto'] = form_anteproyecto

            if existe_solicitud:
                context['existe_solicitud'] = existe_solicitud
                context['nombre_anteproyecto'] = nombre_anteproyecto
                context['fecha_envio'] = content_anteproyecto.fecha_envio
        context['respuestas'] = recuperar_retroalimentacion(
            content_anteproyecto)
        form_proyecto_final = FormProyectoFinal
        context['form_proyecto_final'] = form_proyecto_final
        # Renderizamos la plantilla en cualquier caso.
        return render(request, 'estudiante/solicitud.html', context)
# vista de la informacion del proyecto


@login_required
def info_proyect(request):
    if request.method == 'POST':
        context = contenido_anteproyecto(request)
        return render(request, 'estudiante/Inf_proyect.html', context)
    else:
        context = contenido_anteproyecto(request)
        anteproyecto = ModelAnteproyecto.objects.get(user=request.user)
        retroalimentacion = recuperar_retroalimentacion(anteproyecto)

        if retroalimentacion:
            # recordar que este recibe el documento y la respuesta general en un diccionario
            context['content_retroalimentacion'] = retroalimentacion

            return render(request, 'estudiante/Inf_proyect.html', context)
        else:
            doc_revisado = None
            context['content_retroalimentacion'] = retroalimentacion

            return render(request, 'estudiante/Inf_proyect.html', context)


@login_required
def enviar_solicitud_proyecto(request):
    print(f"Usuario autenticado: {request.user}")
    if request.method == 'POST':
        anteproyecto = recuperar_anteproyecto(request)
        print(f"Anteproyecto: {anteproyecto}")
        form = FormProyectoFinal(request.POST, request.FILES)
        if form.is_valid():
            proyecto_final = form.save(commit=False)
            proyecto_final.user = request.user
            proyecto_final.anteproyecto = anteproyecto
            proyecto_final.descripcion = anteproyecto.descripcion
            proyecto_final.director = anteproyecto.director
            proyecto_final.codirector = anteproyecto.codirector
            proyecto_final.solicitud_enviada = True
            proyecto_final.fecha_envio = fecha_actual()
            form.save()
            print('datos enviados')
            return redirect('estudiante:solicitud')
    return redirect('estudiante:solicitud')
