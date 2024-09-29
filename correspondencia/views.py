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
from plataform_CIGAP.utils.recuperaciones import recuperar_num_proyectos_terminados, recuperar_num_proyectos_pendientes, recuperar_num_solicitudes, recuperar_num_formatos_comite, recuperar_num_respuestas, recuperar_proyectos_pendientes, recuperar_proyectos_finalizados, recuperar_proyecto_finalizado, recuperar_proyecto_actual, recuperar_solicitudes_especiales_proyecto
from plataform_CIGAP.utils.funcionalidades_fechas import fecha_actual

# importacion de los modelos
from estudiante.models import ModelAnteproyecto, ModelProyectoFinal
from login.models import Usuarios
from correspondencia.models import ModelRetroalimentaciones, ModelSolicitudes, ModelAsignacionJurados, ModelDocumentos

# importacion de los formularios
from .forms import FormRetroalimentacionAnteproyecto, FormRetroalimentacionProyecto, FormJurados, FormDocumentos
from estudiante.forms import FormAnteproyecto, FormProyectoFinal, FormActualizarProyectoFinal

# importacion del manejo de clases de vistas
# tener en cuenta para el manejo de clases de vista con cada uno de los metodos y la asignacion de las urls de las mismas con asView
from django.views.generic.edit import CreateView
# from django.views.generic.list import ListView
# from django.urls import reverse_lazy

# Create your views here.
# def funcionando (request):
#     return HttpResponse('app_ correspondencia funcionando.')
########################################################################################################################
# Recuperar informaciones y funciones especificas para las vistas


def recuperar_anteproyectos_pendientes():
    anteproyectos_pendientes = ModelAnteproyecto.objects.filter(
        estado=False, solicitud_enviada=True)
    return anteproyectos_pendientes


def recuperar_proyectos_finales_pendientes():
    proyectos_finales_pendientes = ModelProyectoFinal.objects.filter(solicitud_enviada=True, estado=False
                                                                     )
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
    proyectos_finales = ModelProyectoFinal.objects.filter(
        solicitud_enviada=True)
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


def recuperar_solicitudes_anteproyecto():
    solicitudes = ModelRetroalimentaciones.objects.filter(
        anteproyecto__isnull=False)
    return solicitudes


def recuperar_solicitud(anteproyecto):
    solicitud = ModelRetroalimentaciones.objects.get(
        anteproyecto=anteproyecto) if ModelRetroalimentaciones.objects.filter(anteproyecto=anteproyecto).exists() else None
    return solicitud
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
    num_solicitudes = recuperar_num_solicitudes()
    num_formatos = recuperar_num_formatos_comite()
    num_proyectos = recuperar_num_proyectos_pendientes()
    num_respuestas = recuperar_num_respuestas()

    context['num_solicitudes'] = num_solicitudes
    context['num_formatos'] = num_formatos
    context['num_proyectos'] = num_proyectos
    context['num_respuestas'] = num_respuestas
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

    return render(request, 'correspondencia/views_solicitud/solicitudes.html', context)


def solicitudes_anteproyectos(request):
    context = datosusuario(request)
    if request.method == 'POST':
        pass
    else:
        anteproyectos = recuperar_anteproyectos_pendientes()
        context['anteproyectos'] = anteproyectos

        return render(request, 'correspondencia/views_solicitud/list_anteproyectos.html', context)


def solicitudes_proyectos_finales(request):
    context = datosusuario(request)

    if request.method == 'POST':
        pass
    else:
        proyectos_finales = recuperar_proyectos_finales()
        context['proyectos_finales'] = proyectos_finales
        return render(request, 'correspondencia/views_solicitud/list_proyectos_finales.html', context)

# funcion de la vista de lista de solicitudes especiales


def solicitudes_especiales(request):
    context = datosusuario(request)

    if request.method == 'POST':
        pass
    else:
        solicitudes_especiales = recuperar_solicitudes_especiales_pendientes()
        context["solicitudes_especiales"] = solicitudes_especiales
        return render(request, 'correspondencia/views_solicitud/list_solicitud_especiales.html', context)


def view_solicitud_especial(request, id):
    context = datosusuario(request)

    solicitud_especial = recuperar_solicitud_especial(id)

    context['solicitud_especial'] = solicitud_especial

    documento_binario = solicitud_especial.documento_soporte
    documento_soporte = recuperar_documento(documento_binario)
    context['documento_soporte'] = documento_soporte

    if solicitud_especial.anteproyecto:
        form_anteproyecto = FormAnteproyecto(
            instance=solicitud_especial.anteproyecto)
        form_retroalimentacion_ante = FormRetroalimentacionAnteproyecto(
            instance=solicitud_especial.anteproyecto)
        context['form_anteproyecto'] = form_anteproyecto
        context['form_retroalimentacion'] = form_retroalimentacion_ante
    elif solicitud_especial.proyecto_final:
        form_proyecto_final = FormActualizarProyectoFinal(
            instance=solicitud_especial.proyecto_final)
        form_retroalimentacion_pro = FormRetroalimentacionProyecto(
            instance=solicitud_especial.proyecto_final)
        context['form_proyecto'] = form_proyecto_final
        context['form_retroalimentacion'] = form_retroalimentacion_pro
    else:
        return HttpResponse('Error: No se encontró anteproyecto ni proyecto final.')

    return render(request, 'correspondencia/views_solicitud/solicitud_especial.html', context)


def actualizar_datos_solicitud_anteproyecto(request, id):
    solicitud_especial = recuperar_solicitud_especial(id)
    anteproyecto = solicitud_especial.anteproyecto

    if request.method == 'POST':
        form_anteproyecto = FormAnteproyecto(
            request.POST, request.FILES, instance=anteproyecto)
        if form_anteproyecto.is_valid():
            form_anteproyecto.save()
            return redirect('correspondencia:view_solicitud_especial', id=id)
        else:
            # Mostrar errores del formulario
            return HttpResponse(f'Algo pasó: {form_anteproyecto.errors}')
    return HttpResponse('Terminado')


def actualizar_datos_solicitud_proyecto(request, id):
    context = datosusuario(request)
    solicitud_especial = recuperar_solicitud_especial(id)
    proyecto = solicitud_especial.proyecto_final
    anteproyecto = proyecto.anteproyecto
    if request.method == 'POST':
        form_proyecto = FormActualizarProyectoFinal(
            request.POST, request.FILES, instance=proyecto
        )
        director = request.POST.get('director')
        codirector = request.POST.get('codirector')

        # No se actualizan los archivos si no se envían
        if form_proyecto.is_valid():
            if not request.FILES.get('doc_proyecto_final_form'):
                form_proyecto.cleaned_data.pop('doc_proyecto_final_form', None)
            if not request.FILES.get('carta_presentacion_final_form'):
                form_proyecto.cleaned_data.pop(
                    'carta_presentacion_final_form', None)

            anteproyecto.director = director
            anteproyecto.codirector = codirector
            anteproyecto.save(update_fields=['director', 'codirector'])
            form_proyecto.save()
            return redirect('correspondencia:view_solicitud_especial', id=id)
        else:
            return HttpResponse(f'Error: {form_proyecto.errors}')
    else:
        # Inicializar el formulario con la instancia del proyecto existente
        form_proyecto = FormActualizarProyectoFinal(instance=proyecto)
        context['form_proyecto'] = form_proyecto
    return render(request, 'ruta_de_template.html', context)


def enviar_retroalimentacion_solicitud(request, id):
    solicitud_especial = recuperar_solicitud_especial(id)

    if solicitud_especial.anteproyecto:
        form_retro = FormRetroalimentacionAnteproyecto(
            request.POST, request.FILES)
        if form_retro.is_valid():
            solicitud_especial.estado = True
            solicitud_especial.save()
            retroalimentacion = form_retro.save(commit=False)
            retroalimentacion.anteproyecto = solicitud_especial.anteproyecto
            retroalimentacion.fecha_retroalimentacion = fecha_actual()
            retroalimentacion.revs_dadas = (
                retroalimentacion.revs_dadas or 0) + 1
            retroalimentacion.save()
            return redirect('correspondencia:solicitudes')
        else:
            return HttpResponse(f'Algo paso: {form_retro.errors}')
    else:
        if solicitud_especial.proyecto_final:
            form_retro = FormRetroalimentacionAnteproyecto(
                request.POST, request.FILES)
            if form_retro.is_valid():
                solicitud_especial.estado = True
                solicitud_especial.save()
                retroalimentacion = form_retro.save(commit=False)
                retroalimentacion.proyecto_final = solicitud_especial.proyecto_final
                retroalimentacion.fecha_retroalimentacion = fecha_actual()
                retroalimentacion.revs_dadas = (
                    retroalimentacion.revs_dadas or 0) + 1
                retroalimentacion.save()
                return redirect('correspondencia:solicitudes')
            else:
                return HttpResponse(f'Algo paso: {form_retro.errros}')

    return HttpResponse(solicitud_especial)
########################################################################################################################
# vista para conocer la informacion del anteproyecto


def ver_anteproyecto(request, nombre_anteproyecto):
    context = datosusuario(request)
    directores = recuperar_directores()
    if directores:
        context['directores'] = directores
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
                nuevo_proyecto_final = ModelProyectoFinal(
                    user=request.user,
                    anteproyecto=anteproyecto,
                )
                nuevo_proyecto_final.save()
                retroalimentacion.save()
            if retroalimentacion.doc_retroalimentacion:
                print("Documento subido correctamente")
            else:
                print("Error al subir el documento")
            return redirect('correspondencia:solicitudes')
        else:
            print(form_retro.errors)

    return redirect('correspondencia:solicitudes')


# vista de informacion de proyecto


def ver_proyecto_final(request, nombre):
    context = datosusuario(request)
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
                return render('correspondenicia:solicitudes')

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
            url = reverse('correspondencia:asignar_jurados',
                          kwargs={'nombre': nombre})
            return redirect(url)

        else:
            print(form_retro.errors)  # Para depuración
    else:

        anteproyecto = recuperar_anteproyecto(nombre)
        if anteproyecto:

            proyecto_final = recuperar_proyecto_final(anteproyecto)
            if proyecto_final:

                doc_proyecto_final = recuperar_documento(
                    proyecto_final.proyecto_final)
                doc_carta_final = recuperar_documento(
                    proyecto_final.carta_presentacion_final)
                context['inf_proyecto'] = proyecto_final
                context['doc_proyecto_final'] = doc_proyecto_final
                context['doc_carta_final'] = doc_carta_final

        directores = recuperar_directores()

        context['directores'] = directores
        form_retroalimentaciones_proyecto = FormRetroalimentacionProyecto
        form_jurados = FormJurados
        context['form_jurados'] = form_jurados
        context['form_retroalimentacion'] = form_retroalimentaciones_proyecto
        return render(request, 'correspondencia/views_solicitud/proyecto.html', context)

# tener en cuenta la lgoca de javaScript con el fin de que si es aprovado, muestre el formurio de la asignacion de jurados
# asi mismo crear la vista de enviar retroalimentaicon de proyecto


def asignar_jurados(request, nombre):
    context = datosusuario(request)
    nombre_proyecto = nombre

    if request.method == 'POST':
        directores_seleccionados = request.POST.getlist('directores')
        fecha_sustentacion_str = request.POST.get('fecha_sustentacion')
        fecha_sustentacion = datetime.fromisoformat(
            str(fecha_sustentacion_str)).date()

        asignacion_jurados = ModelAsignacionJurados()
        anteproyecto = recuperar_anteproyecto(nombre_proyecto)
        proyecto_final = recuperar_proyecto_aceptado(anteproyecto)

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

            proyecto_final = recuperar_proyecto_final(anteproyecto)
            if proyecto_final:

                context['inf_proyecto'] = proyecto_final

        directores = recuperar_directores()
        context['directores'] = directores
        context['proyecto'] = anteproyecto

        if anteproyecto.director and anteproyecto.codirector:
            director = Usuarios.objects.get(nombre_completo=anteproyecto.director) if Usuarios.objects.filter(
                nombre_completo=anteproyecto.director).exists() else None
            codirector = Usuarios.objects.get(nombre_completo=anteproyecto.codirector) if Usuarios.objects.filter(
                nombre_completo=anteproyecto.codirector).exists() else None
            imagen_director = recuperar_documento(director.imagen)
            context['img_director'] = imagen_director
            if codirector:
                imagen_codirector = recuperar_documento(codirector.imagen)
                context['img_codirector'] = imagen_codirector
        else:
            director = Usuarios.objects.get(nombre_completo=anteproyecto.director) if Usuarios.objects.filter(
                nombre_completo=anteproyecto.director).exists() else None
            imagen_director = recuperar_documento(director.imagen)
            context['img_director'] = imagen_director

        form_jurados = FormJurados()
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
    context = datosusuario(request)

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

            documento_respuesta = recuperar_documento(doc_binario)
            context['documento_respuesta'] = documento_respuesta
            context['respuesta'] = respuesta

            return render(request, 'correspondencia/views_respuestas/visualizacion_respuesta.html', context)
    return render(request, 'correspondencia/views_respuestas/visualizacion_respuesta.html')


########################################################################################################################
# vista de documentos cargados por los estudiantes
# def documentos_cargados(request):
#     return render(request, 'correspondencia/list_documentos_cargados.html')
########################################################################################################################


def recuperar_formatos():
    documentos_model = ModelDocumentos.objects.all()
    documentos = {}
    if documentos_model:
        for i, documento in enumerate(documentos_model):
            documento_binario = documento.documento
            documento_convert = recuperar_documento(documento_binario)
            documentos[f'documento{i}'] = {
                'id': documento.id,
                'nombre_documento': documento.nombre_documento,
                'descripcion': documento.descripcion,
                'version': documento.version,
                'documento': documento_convert,
                'fecha_cargue': documento.fecha_cargue
            }
    else:
        documentos = None

    return documentos

############################################################################


def formatos_documentos(request):
    context = datosusuario(request)
    if request.method == 'POST':
        form_cargar_docs = FormDocumentos(request.POST, request.FILES)
        if form_cargar_docs.is_valid():
            cargar_documentos = form_cargar_docs.save(commit=False)
            cargar_documentos.fecha_cargue = fecha_actual()
            cargar_documentos.save()
        else:
            return HttpResponse(f'Error: {form_cargar_docs.errors}')
    else:
        form_cargar_docs = FormDocumentos
        context['formatos'] = recuperar_formatos()
        context['form_cargar_docs'] = form_cargar_docs

    return render(request, 'correspondencia/views_formatos/documentos_comite.html', context)


# funcion para eliminar un formato cargado
def eliminar_formato(request, id):
    formato_id = id
    formato = ModelDocumentos.objects.get(id=formato_id)
    formato.delete()
    return redirect('correspondencia:formatos_documentos')


# funcion para editar un formato
def editar_formato(request, id):
    formato = ModelDocumentos.objects.get(id=id)

    if request.method == 'POST':
        form_cargar_docs = FormDocumentos(
            request.POST, request.FILES, instance=formato)
        if form_cargar_docs.is_valid():
            form_cargar_docs.save()
            return redirect('correspondencia:formatos_documentos')

            # return redirect('nombre_de_tu_vista_de_exito')  # Redirige a una vista de éxito
    else:
        form_cargar_docs = FormDocumentos(instance=formato)

    doc_convert = formato.documento
    documento = recuperar_documento(doc_convert)
    context = {
        'form_edit': form_cargar_docs,
        'documento': documento,
    }
    return render(request, 'correspondencia/views_formatos/formato.html', context)
#####################################################################################################################
# apartado de la lista de proyectos


def proyectos(request):
    context = datosusuario(request)
    num_proyectos_terminados = recuperar_num_proyectos_terminados()
    num_proyectos_actuales = recuperar_num_proyectos_pendientes()
    context['num_proyectos_actuales'] = num_proyectos_actuales
    context['num_proyectos_terminados'] = num_proyectos_terminados
    return render(request, 'correspondencia/views_proyectos/proyectos.html', context)


def proyectos_finalizados(request):
    context = datosusuario(request)
    list_proyectos_finalizados = recuperar_proyectos_finalizados()
    dic_proyectos = {}
    if list_proyectos_finalizados:

        for i, proyecto in enumerate(list_proyectos_finalizados):
            documento_convert = proyecto.proyecto_final
            documento = recuperar_documento(documento_convert)

            dic_proyectos[f'proyecto{i}'] = {
                'proyecto': proyecto,
                'documento_convert': documento
            }
        context['proyectos'] = dic_proyectos
    return render(request, 'correspondencia/views_proyectos/list_proyectos_finalizados.html', context)


def proyectos_actuales(request):
    context = datosusuario(request)
    proyectos_actuales = recuperar_proyectos_pendientes()
    dic_proyectos = {}
    if proyectos_actuales:
        for i, proyecto in enumerate(proyectos_actuales):
            documento_convert_carta = proyecto.carta_presentacion
            documento_convert_ante = proyecto.anteproyecto
            documento_carta = recuperar_documento(documento_convert_carta)
            documento_ante = recuperar_documento(documento_convert_ante)

            dic_proyectos[f'proyecto{i}'] = {
                'proyecto': proyecto,
                'documento_ante': documento_ante,
                'documento_carta': documento_carta
            }
        context['proyectos'] = dic_proyectos
    return render(request, 'correspondencia/views_proyectos/list_proyectos_actuales.html', context)


def proyecto_final(request, id):
    context = datosusuario(request)

    proyecto = recuperar_proyecto_finalizado(id)
    # return HttpResponse(
    #     proyecto
    # )
    integrantes = (proyecto.anteproyecto.nombre_integrante1, proyecto.anteproyecto.nombre_integrante2,
                   proyecto.anteproyecto.director, proyecto.anteproyecto.codirector)
    datos_integrantes = {}
    for i, integrante in enumerate(integrantes, start=1):
        if integrante:
            datos_integrantes[f'integrante_{i}'] = recuperar_datos_integrantes(
                integrante)
        context['datos_integrantes'] = datos_integrantes
    context['proyecto'] = proyecto
    carta_convert = recuperar_documento(
        proyecto.anteproyecto.carta_presentacion)
    ante_convert = recuperar_documento(proyecto.anteproyecto.anteproyecto)
    carta_final_convert = recuperar_documento(
        proyecto.carta_presentacion_final)
    proyecto__final_convert = recuperar_documento(proyecto.proyecto_final)


# añadir la logica de solicitudes pesepciales tambien pero para el proyecto finalizado

    retroalimentaciones = recuperar_solicitudes_anteproyecto()

    if retroalimentaciones:
        dic_retroalimentaciones = {}
        for i, retroalimentacion in enumerate(retroalimentaciones):

            dic_retroalimentaciones[f'retroalimentacion{i}'] = {
                'doc_retroalimentacion': recuperar_documento(retroalimentacion.doc_retroalimentacion),
                'fecha_retroalimentacion': retroalimentacion.fecha_retroalimentacion,
                'respuesta': retroalimentacion.retroalimentacion,
            }

            context['retroalimentaciones'] = dic_retroalimentaciones

        context['formatos'] = {
            'anteproyecto': ante_convert,
            'carta_presentacion': carta_convert,
            'anteproyecto': ante_convert,
            'proyecto__final_convert': carta_final_convert
        }

    # apartado para recuperar cada una de las solicitudes especiales
    solicitudes_especiales = recuperar_solicitudes_especiales_proyecto(
        proyecto, proyecto.anteproyecto)
    dict_solicitudes = {}
    if solicitudes_especiales:
        for i, solicitud_especial in enumerate(solicitudes_especiales):
            dict_solicitudes[f'solicitud{i}'] = {
                'doc_solicitudes': solicitud_especial.documento_soporte,
                'fecha_envio': solicitud_especial.fecha_envio,
            }
        context['solicitudes'] = dict_solicitudes
    return render(request, 'correspondencia/views_proyectos/proyecto_finalizado.html', context)


def proyecto_actual(request, id):
    context = datosusuario(request)
    proyecto = recuperar_proyecto_actual(id)
    integrantes = (proyecto.nombre_integrante1, proyecto.nombre_integrante2,
                   proyecto.director, proyecto.codirector)
    datos_integrantes = {}
    for i, integrante in enumerate(integrantes, start=1):
        if integrante:
            datos_integrantes[f'integrante_{i}'] = recuperar_datos_integrantes(
                integrante)
        context['datos_integrantes'] = datos_integrantes
    context['proyecto'] = proyecto
    carta_convert = recuperar_documento(proyecto.carta_presentacion)
    ante_convert = recuperar_documento(proyecto.anteproyecto)


# añadir la logica de solicitudes pesepciales tambien pero para el proyecto finalizado

    retroalimentaciones = recuperar_solicitudes_anteproyecto()

    if retroalimentaciones:
        dic_retroalimentaciones = {}
        for i, retroalimentacion in enumerate(retroalimentaciones):

            dic_retroalimentaciones[f'retroalimentacion{i}'] = {
                'doc_retroalimentacion': recuperar_documento(retroalimentacion.doc_retroalimentacion),
                'fecha_retroalimentacion': retroalimentacion.fecha_retroalimentacion,
                'respuesta': retroalimentacion.retroalimentacion,
            }

            context['retroalimentaciones'] = dic_retroalimentaciones

        context['formatos'] = {
            'anteproyecto': ante_convert,
            'carta_presentacion': carta_convert
        }
    return render(request, 'correspondencia/views_proyectos/proyecto_actual.html', context)
#####################################################################################################################
