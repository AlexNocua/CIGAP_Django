import django.contrib.auth
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from plataform_CIGAP.views import logout_user
from django.contrib.auth.decorators import login_required
import base64
# importacion de operadores para consultas de django
from django.db.models import Q

# importacion de la vista del login que permite cambiar la informacion de ususario
from login.views import editar_usuario
from login.forms import FormEditarUsuario
# importacion de las funcionalidaes
from plataform_CIGAP.utils.decoradores import grupo_usuario
from plataform_CIGAP.utils.funcionalidades_fechas import fecha_actual

# importacion de los modelos
from estudiante.models import ModelAnteproyecto, ModelProyectoFinal
from login.models import Usuarios
from correspondencia.models import ModelRetroalimentaciones, ModelSolicitudes


# importacion de los formularios

from .forms import FormRetroalimentacionAnteproyecto
from estudiante.forms import FormAnteproyecto


# Create your views here.
# def funcionando (request):
#     return HttpResponse('app_ correspondencia funcionando.')
########################################################################################################################
# Recuperar informaciones y funciones especificas para las vistas

def recuperar_anteproyectos_pendientes():
    anteproyectos_pendientes = ModelAnteproyecto.objects.filter(estado=False)
    return anteproyectos_pendientes


def recuperar_proyectos_finales_pendientes():
    proyectos_finales_pendientes = ModelProyectoFinal.objects.filter(
        estado=False)
    return proyectos_finales_pendientes


def recuperar_solicitudes_especiales_pendientes():
    solicitudes_pendientes = ModelSolicitudes.objects.filter(
        Q(estado=False) & (Q(tipo_solicitud='cambio_nombre') | Q(
            tipo_solicitud='ajuste_integrantes') | Q(tipo_solicitud='seccion_derechos') | Q(tipo_solicitud='otro'))
    )
    print(solicitudes_pendientes.count())
    return solicitudes_pendientes
# funcion para traer los anteproyectos


def recuperar_anteproyectos():
    anteproyectos = ModelAnteproyecto.objects.all()
    return anteproyectos

# funcion para traer un anteproyecto en especifico


def recuperar_anteproyecto(nombre):
    anteproyecto = ModelAnteproyecto.objects.get(
        nombre_anteproyecto=nombre) if ModelAnteproyecto.objects.filter(nombre_anteproyecto=nombre).exists() else None
    return anteproyecto


# funcion para recuperar un proyecto Final
def recuperar_proyecto_final(anteproyecto):
    proyecto_final = ModelProyectoFinal.objects.get(
        anteproyecto=anteproyecto) if ModelProyectoFinal.objects.filter(anteproyecto=anteproyecto).exists else None
    return proyecto_final

# funcion para recuperar proyectos finales


def recuperar_proyectos_finales():
    proyectos_finales = ModelProyectoFinal.objects.all()
    return proyectos_finales

# funcion para recuperar una solicitud espeial


def recuperar_solicitud_especial():
    solicitud_especial = ModelSolitudes.objects.get()
    return solicitud_especial

# funcion para recuperar solicitudes espeiales


def recuperar_solicitudes_especiales():
    solicitudes_especiales = ModelSolicitudes.objects.all()
    return solicitudes_especiales
# funcion para recuperar las imagenes de los usuarios


def recuperar_datos_integrantes(nombre):
    usuario = Usuarios.objects.get(nombre_completo=nombre) if Usuarios.objects.filter(
        nombre_completo=nombre).exists() else False
    if usuario:
        imagen_binaria = usuario.imagen
        imagen = base64.b64encode(imagen_binaria).decode(
            'utf8') if imagen_binaria else False
        grupos = usuario.groups.values_list('name', flat=True)
        grupo = 'Estudiante' if 'Estudiantes' in grupos else 'Director' if 'Directores' in grupos else 'Desconocido'
        return {'nombre': nombre, 'imagen': imagen, 'grupo': grupo}
    else:
        return {'nombre': nombre, 'imagen': False, 'grupo': 'Desconocido'}


# funcion para traer la lista de solicitudes
def recuperar_solicitudes():
    solicitudes = ModelRetroalimentaciones.objects.all()
    # context = {
    #     # 'nombre_anteproyecto': solicitudes.anteproyecto.nombre_anteproyecto,
    #     'retroalimentacion': solicitudes.retroalimentacion,
    #     'fecha_retroalimentacion': solicitudes.fecha_retroalimentacion,
    #     'doc_retroalimentacion': solicitudes.doc_retroalimentacion,
    #     'estado': solicitudes.estado,
    #     'revs_dadas': solicitudes.revs_dadas,

    # }
    return solicitudes

# funcion de recuperar documento binario


def recuperar_documento(documento):
    documento = base64.b64encode(documento).decode(
        'utf-8') if documento else None
    return documento


@login_required
def datosusuario(request):

    usuario = request.user
    imagen = usuario.imagen
    imagen_convertida = base64.b64encode(
        imagen).decode('utf-8') if imagen else ''
    form_editar_usuario = FormEditarUsuario(instance=usuario)
    form_solicitud = FormAnteproyecto
    context = {'form_config': form_editar_usuario, 'usuario': usuario,
               'user_img': imagen_convertida}
    return context


@login_required
@grupo_usuario('Correspondencia')
def principal_correspondencia(request):
    context = datosusuario(request)
    return render(request, 'correspondencia/base_correspondencia.html', context)

########################################################################################################################
# vista de solicitudes


@grupo_usuario('Correspondencia')
def solicitudes(request):
    context = datosusuario(request)
    proyectos_finales_pendientes = recuperar_proyectos_finales_pendientes()
    solicitudes_especiales_pendientes = recuperar_solicitudes_especiales_pendientes()
    anteproyectos_pendientes = recuperar_anteproyectos_pendientes()

    context['proyectos_finales'] = proyectos_finales_pendientes.count()
    context['solicitudes_especiales'] = solicitudes_especiales_pendientes.count()
    context['anteproyectos'] = anteproyectos_pendientes.count()

    total_pendientes = proyectos_finales_pendientes.count(
    ) + solicitudes_especiales_pendientes.count() + anteproyectos_pendientes.count()
    context['solicitudes_pendientes'] = total_pendientes

    return render(request, 'correspondencia/solicitudes.html', context)


def solicitudes_anteproyectos(request):
    context = {}
    if request.method == 'POST':
        pass
    else:
        anteproyectos = recuperar_anteproyectos()
        context['anteproyectos'] = anteproyectos
        print(anteproyectos)
        return render(request, 'correspondencia/views_solicitud/list_anteproyectos.html', context)


def solicitudes_proyectos_finales(request):
    context = {}

    if request.method == 'POST':
        pass
    else:
        proyectos_finales = recuperar_proyectos_finales()
        context['proyectos_finales']= proyectos_finales
        return render(request, 'correspondencia/views_solicitud/list_proyectos_finales.html', context)


def solicitudes_especiales(request):
    context = {}

    if request.method == 'POST':
        pass
    else:
        var_solicitudes_especiales = recuperar_solicitudes_especiales()
        context["solicitudes_especiales"]=var_solicitudes_especiales
        return render(request, 'correspondencia/views_solicitud/list_solicitud_especiales.html',context)

########################################################################################################################
# vista para conocer la informacion del proyecto


def ver_anteproyecto(request, nombre_anteproyecto):
    context = datosusuario(request)
    anteproyecto = recuperar_anteproyecto(nombre_anteproyecto)
    doc_anteproyecto = recuperar_documento(anteproyecto.anteproyecto)
    doc_carta = recuperar_documento(anteproyecto.carta_presentacion)
    context['inf_anteproyecto'] = {'anteproyecto': anteproyecto,
                                   'form_retroalimentacion': FormRetroalimentacionAnteproyecto,
                                   'doc_anteproyecto': doc_anteproyecto,
                                   'doc_carta': doc_carta}

    if anteproyecto:
        integrantes = (anteproyecto.nombre_integrante1, anteproyecto.nombre_integrante2,
                       anteproyecto.director, anteproyecto.codirector)
        datos_integrantes = {}
        for i, integrante in enumerate(integrantes, start=1):
            if integrante:
                datos_integrantes[f'integrante_{i}'] = recuperar_datos_integrantes(
                    integrante)
        context['datos_integrantes'] = datos_integrantes
        return render(request, 'correspondencia/anteproyecto.html', context)
    else:
        return HttpResponse('Gestiona los proyectos existentes, algo pasó con este.')


def enviar_retroalimentacion(request, nombre_anteproyecto):
    anteproyecto = recuperar_anteproyecto(nombre_anteproyecto)
    if anteproyecto is None:
        return HttpResponse('Error: Anteproyecto no encontrado')

    if request.method == 'POST':
        form_retro = FormRetroalimentacionAnteproyecto(
            request.POST, request.FILES)
        if form_retro.is_valid():
            retroalimentacion = form_retro.save(commit=False)
            retroalimentacion.anteproyecto = anteproyecto
            retroalimentacion.fecha_retroalimentacion = fecha_actual()
            retroalimentacion.revs_dadas = (
                retroalimentacion.revs_dadas or 0) + 1
            retroalimentacion.save()
            if retroalimentacion.doc_retroalimentacion:
                print("Documento subido correctamente")
            else:
                print("Error al subir el documento")
            return redirect('correspondencia:solicitudes')
        else:
            print(form_retro.errors)  # Para depuración

    return redirect('correspondencia:solicitudes')
########################################################################################################################

# listado de solicitudes


def solicitudes_respondidas(request):
    respuestas = recuperar_solicitudes()
    print(respuestas)
    context = datosusuario(request)
    respuestas_dict = {}
    for i, respuesta in enumerate(respuestas):
        doc_binario = recuperar_documento(respuesta.doc_retroalimentacion)
        respuestas_dict[f'respuesta_{i}'] = {
            'respuesta': respuesta, 'doc_binario': doc_binario}
    context['respuestas'] = respuestas_dict
    return render(request, 'correspondencia/list_solicitudes_anteproyecto.html', context)


########################################################################################################################
# vista de documentos cargados por los estudinates
def documentos_cargados(request):
    return render(request, 'correspondencia/list_documentos_cargados.html')
########################################################################################################################


def formatos_documentos(request):
    return render(request, 'correspondencia/documentos_comite.html')
