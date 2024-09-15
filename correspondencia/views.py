from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from plataform_CIGAP.views import logout_user
from django.contrib.auth.decorators import login_required
import base64
from datetime import datetime
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
from correspondencia.models import ModelRetroalimentaciones, ModelSolicitudes, ModelAsignacionJurados


# importacion de los formularios

from .forms import FormRetroalimentacionAnteproyecto, FormRetroalimentacionProyecto, FormJurados
from estudiante.forms import FormAnteproyecto, FormProyectoFinal

# importacion del manejo de clases de vistas
# tener en cuenta para el manejo de clases de vista con cada uno de los metodos y la asignacion de las urls de las mismas con asView
from django.views.generic.edit import CreateView
# from django.views.generic.list import ListView
# from django.urls import reverse_lazy


# realizar el filtro por ususarios de la plataforma, designando solo los que pertenezcan a directro


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


def recuperar_proyectos_finales_finalizados():
    proyectos_finales_finalizados = ModelProyectoFinal.objects.filter(
        estado=True)
    return proyectos_finales_finalizados


def recuperar_asignaciones_jurados():
    pass


def recuperar_solicitudes_especiales_pendientes():
    solicitudes_pendientes = ModelSolicitudes.objects.filter(
        Q(estado=False) & (Q(tipo_solicitud='cambio_nombre') | Q(
            tipo_solicitud='ajuste_integrantes') | Q(tipo_solicitud='seccion_derechos') | Q(tipo_solicitud='otro'))
    )

    return solicitudes_pendientes


def recuperar_solicitud_especial_pendiente(id):
    solicitud_pendiente = ModelSolicitudes.objects.get(
        id=id) if ModelSolicitudes.objects.filter(id=id).exists() else None
    return solicitud_pendiente
# funcion para traer los anteproyectos


def recuperar_anteproyectos():
    anteproyectos = ModelAnteproyecto.objects.all()
    return anteproyectos

# funcion para recuperar los anteproyectos que aun no estan aprovados


def recuperar_anteproyectos_pendientes():
    anteproyectos = ModelAnteproyecto.objects.filter(estado=False)
    return anteproyectos
# funcion para traer un anteproyecto en especifico


def recuperar_anteproyecto(nombre):
    anteproyecto = ModelAnteproyecto.objects.get(nombre_anteproyecto=nombre) if ModelAnteproyecto.objects.filter(
        nombre_anteproyecto=nombre).exists() else None
    return anteproyecto

# funcion para recuperar un proyecto Final


def recuperar_proyecto_final(anteproyecto):
    proyecto_final = ModelProyectoFinal.objects.get(
        anteproyecto=anteproyecto) if ModelProyectoFinal.objects.filter(anteproyecto=anteproyecto).exists() else None
    return proyecto_final

# funcion para recuperar proyectos finales


def recuperar_proyecto_aceptado(anteproyecto):
    proyecto_final = ModelProyectoFinal.objects.get(
        anteproyecto=anteproyecto, estado=True) if ModelProyectoFinal.objects.filter(anteproyecto=anteproyecto).exists() else None
    return proyecto_final


def recuperar_proyectos_finales():
    proyectos_finales = ModelProyectoFinal.objects.all()
    return proyectos_finales

# funcion para recuperar una solicitud espeial


def recuperar_solicitud_especial(id):
    solicitud_especial = ModelSolicitudes.objects.get(
        id=id) if ModelSolicitudes.objects.filter(id=id).exists() else None
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
    return solicitudes
# def recuperar_solicitudes_():
#     solicitudes = ModelRetroalimentaciones.objects.filter(anteproyecto=True)
#     return solicitudes

# funcion de recuperar documento binario


def recuperar_documento(documento):
    documento = base64.b64encode(documento).decode(
        'utf-8') if documento else None
    return documento

# funcion para recuperar datos de los directores


def recuperar_directores():
    directores = Usuarios.objects.filter(
        groups__name="Directores").values('nombre_completo', 'email')
    if directores:
        return directores
    else:
        directores = None
        return directores


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
        anteproyectos = recuperar_anteproyectos_pendientes()
        context['anteproyectos'] = anteproyectos
        print(anteproyectos)
        return render(request, 'correspondencia/views_solicitud/list_anteproyectos.html', context)


def solicitudes_proyectos_finales(request):
    context = {}

    if request.method == 'POST':
        pass
    else:
        proyectos_finales = recuperar_proyectos_finales()
        context['proyectos_finales'] = proyectos_finales
        return render(request, 'correspondencia/views_solicitud/list_proyectos_finales.html', context)

# funcion de la vista de lista de solicitudes especiales


def solicitudes_especiales(request):
    context = {}

    if request.method == 'POST':
        pass
    else:
        solicitudes_especiales = recuperar_solicitudes_especiales_pendientes()
        context["solicitudes_especiales"] = solicitudes_especiales
        return render(request, 'correspondencia/views_solicitud/list_solicitud_especiales.html', context)


def view_solicitud_especial(request, id):
    context = {
    }

    solicitud_especial = recuperar_solicitud_especial(id)
    if solicitud_especial.anteproyecto:
        form_anteproyecto = FormAnteproyecto
        context['form_proyecto'] = FormAnteproyecto
        context ['form_retroalimentacion'] = FormRetroalimentacionAnteproyecto
        form_retroalimentacion_ante = FormRetroalimentacionAnteproyecto
    else:
        if solicitud_especial.proyecto_final:   
            form_retroalimentacion_pro = FormRetroalimentacionProyecto
            form_proyecto_final = FormProyectoFinal
            context['form_proyecto'] = FormProyectoFinal
            context['form_retroalimentacion'] = FormRetroalimentacionProyecto
        else:
            return HttpResponse('Error')
        
    return render(request, 'correspondencia/views_solicitud/solicitud_especial.html', context)


def actualizar_datos_solicitud():
    pass


def enviar_retroalimentacion_solicitud():
    pass
########################################################################################################################
# vista para conocer la informacion del anteproyecto


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
        return render(request, 'correspondencia/views_solicitud/anteproyecto.html', context)
    else:
        return HttpResponse('Gestiona los proyectos existentes, algo pasó con este.')


def enviar_retroalimentacion(request, nombre_anteproyecto):
    anteproyecto = recuperar_anteproyecto(nombre_anteproyecto)
    if anteproyecto is None:
        return redirect('correspondencia:solicitudes')

    if request.method == 'POST':
        form_retro = FormRetroalimentacionAnteproyecto(
            request.POST, request.FILES)
        if form_retro.is_valid():
            retroalimentacion = form_retro.save(commit=False)
            retroalimentacion.anteproyecto = anteproyecto
            retroalimentacion.fecha_retroalimentacion = fecha_actual()
            retroalimentacion.revs_dadas = (
                retroalimentacion.revs_dadas or 0) + 1
            if retroalimentacion.estado not in ['Aprobado', 'Aprobado_con_correcciones']:
                anteproyecto.delete()

            else:
                anteproyecto.estado = True
                # salvar las informaciones
                anteproyecto.save(update_fields=['estado',])
                retroalimentacion.save()
            if retroalimentacion.doc_retroalimentacion:
                print("Documento subido correctamente")
            else:
                print("Error al subir el documento")
            return redirect('correspondencia:solicitudes')
        else:
            print(form_retro.errors)  # Para depuración

    return redirect('correspondencia:solicitudes')


# vista de informacion de proyecto


def ver_proyecto_final(request, nombre):
    context = {}
    anteproyecto = recuperar_anteproyecto(nombre)
    proyecto_final = recuperar_proyecto_final(anteproyecto)
    if anteproyecto is None or proyecto_final is None:
        return redirect('correspondencia:solicitudes')
    else:
        integrantes = (anteproyecto.nombre_integrante1, anteproyecto.nombre_integrante2,
                       anteproyecto.director, anteproyecto.codirector)
        datos_integrantes = {}
        for i, integrante in enumerate(integrantes, start=1):
            if integrante:
                datos_integrantes[f'integrante_{i}'] = recuperar_datos_integrantes(
                    integrante)
        context['datos_integrantes'] = datos_integrantes
    if request.method == 'POST':
        form_retro = FormRetroalimentacionAnteproyecto(
            request.POST, request.FILES)

        if form_retro.is_valid():
            retroalimentacion = form_retro.save(commit=False)
            retroalimentacion.proyecto_final = proyecto_final
            retroalimentacion.fecha_retroalimentacion = fecha_actual()
            retroalimentacion.revs_dadas = (
                retroalimentacion.revs_dadas or 0) + 1
            if retroalimentacion.estado not in ['Aprobado', 'Aprobado_con_correcciones']:
                proyecto_final.delete()
                return render('correspondenicia:solicitudesF')

            else:
                proyecto_final.estado = True
                proyecto_final.save(update_fields=['estado',])
                retroalimentacion.save()
                # revisar esta direccion para el envio de datos de retroalimentacones

            if retroalimentacion.doc_retroalimentacion:
                print("Documento subido correctamente")
            else:
                print("Error al subir el documento")
            # tener en cuenta el envio de datos desde url
            url = reverse('correspondencia:asignar_jurados')
            return redirect(f"{url}?nombre_proyecto={nombre}")

        else:
            print(form_retro.errors)  # Para depuración
    else:

        anteproyecto = recuperar_anteproyecto(nombre)
        if anteproyecto:
            print(anteproyecto)
            proyecto_final = recuperar_proyecto_final(anteproyecto)
            if proyecto_final:
                print(proyecto_final)
                context['inf_proyecto'] = proyecto_final

        directores = recuperar_directores()
        print(directores)
        context['directores'] = directores
        form_retroalimentaciones_proyecto = FormRetroalimentacionProyecto
        form_jurados = FormJurados
        context['form_jurados'] = form_jurados
        context['form_retroalimentacion'] = form_retroalimentaciones_proyecto
        return render(request, 'correspondencia/views_solicitud/proyecto.html', context)

# tener en cuenta la lgoca de javaScript con el fin de que si es aprovado, muestre el formurio de la asignacion de jurados
# asi mismo crear la vista de enviar retroalimentaicon de proyecto


def asignar_jurados(request):
    context = {}
    nombre_proyecto = request.GET.get('nombre_proyecto')
    print(nombre_proyecto)
    if request.method == 'POST':
        directores_seleccionados = request.POST.getlist('directores')
        fecha_sustentacion_str = request.POST.get('fecha_sustentacion')
        fecha_sustentacion = datetime.fromisoformat(
            str(fecha_sustentacion_str)).date()

        asignacion_jurados = ModelAsignacionJurados()
        anteproyecto = recuperar_anteproyecto(nombre_proyecto)
        proyecto_final = recuperar_proyecto_aceptado(anteproyecto)
        print(proyecto_final)
        # ajustes en el modelo especifico de proyecto

        asignacion_jurados.proyecto_final = proyecto_final
        asignacion_jurados.nombre_jurado = ', '.join(directores_seleccionados)
        asignacion_jurados.fecha_sustentacion = fecha_sustentacion
        asignacion_jurados.save()
        proyecto_final.jurado = asignacion_jurados

        proyecto_final.save(update_fields=['jurado'])
        return redirect('correspondencia:solicitudes')
    else:
        anteproyecto = recuperar_anteproyecto(nombre_proyecto)
        if anteproyecto:
            print(anteproyecto)
            proyecto_final = recuperar_proyecto_final(anteproyecto)
            if proyecto_final:
                print(proyecto_final)
                context['inf_proyecto'] = proyecto_final

        directores = recuperar_directores()

        context['directores'] = directores
        form_jurados = FormJurados
        context['form_jurados'] = form_jurados

        return render(request, 'correspondencia/views_solicitud/asignacion_jurados.html', context)


########################################################################################################################

# listado de solicitudes


def solicitudes_respondidas(request):
    respuestas = recuperar_solicitudes()
    context = datosusuario(request)
    respuestas_dict = {}
    for i, respuesta in enumerate(respuestas):
        doc_binario = recuperar_documento(respuesta.doc_retroalimentacion)
        if respuesta.proyecto_final:
            print('aqui esta el proyecto')
            respuestas_dict[f'respuesta_{i}'] = {
                'respuesta_proyecto_final': respuesta, 'doc_binario': doc_binario}
        elif respuesta.anteproyecto:
            print('aqui esta el anteproyecto')
            respuestas_dict[f'respuesta_{i}'] = {
                'respuesta_anteproyecto': respuesta, 'doc_binario': doc_binario}
    context['respuestas'] = respuestas_dict

    return render(request, 'correspondencia/views_respuestas/list_solicitudes_respondidas.html', context)

# vista de la respuesta mas detallada


def ver_respuesta(request, id):
    context = {}

    if id:

        respuesta = ModelRetroalimentaciones.objects.get(
            id=id) if ModelRetroalimentaciones.objects.filter(id=id).exists() else 'None'
        if respuesta.anteproyecto:
            integrantes = (respuesta.anteproyecto.nombre_integrante1, respuesta.anteproyecto.nombre_integrante2,
                           respuesta.anteproyecto.director, respuesta.anteproyecto.codirector)
        elif respuesta.proyecto_final:
            integrantes = (respuesta.proyecto_final.anteproyecto.nombre_integrante1, respuesta.proyecto_final.anteproyecto.nombre_integrante2,
                           respuesta.proyecto_final.anteproyecto.director, respuesta.proyecto_final.anteproyecto.codirector)

        if respuesta:
            datos_integrantes = {}
            for i, integrante in enumerate(integrantes, start=1):
                if integrante:
                    datos_integrantes[f'integrante_{i}'] = recuperar_datos_integrantes(
                        integrante)
            context['datos_integrantes'] = datos_integrantes

            doc_binario = respuesta.doc_retroalimentacion
            print(doc_binario)
            documento_respuesta = recuperar_documento(doc_binario)
            context['documento_respuesta'] = documento_respuesta
            context['respuesta'] = respuesta

            return render(request, 'correspondencia/views_respuestas/visualizacion_respuesta.html', context)
    return render(request, 'correspondencia/views_respuestas/visualizacion_respuesta.html')


########################################################################################################################
# vista de documentos cargados por los estudinates
def documentos_cargados(request):
    return render(request, 'correspondencia/list_documentos_cargados.html')
########################################################################################################################


def formatos_documentos(request):
    return render(request, 'correspondencia/documentos_comite.html')
