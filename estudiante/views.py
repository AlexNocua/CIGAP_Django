
# get_object_or_404 para el manejo de errores si no se encuentra un modelo con los siguientes datos
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


from django.contrib.auth.decorators import login_required
# formularios
from correspondencia.forms import FormSolicitudes
from .forms import FormAnteproyecto, FormProyectoFinal, FormObjetivoGeneral, FormObjetivosEspecificos, FormActividades
# modelos
from .models import ModelAnteproyecto, ModelProyectoFinal
import base64
# modelo de correspondencia
from correspondencia.models import ModelRetroalimentaciones

# importacion de modelos del director
from director.models import ModelEvaluacionAnteproyecto, ModelEvaluacionProyectoFinal
# importacion de la vista del login que permite cambiar la informacion de ususario
from login.views import editar_usuario
# importacion del formulario para editar el usuario
from login.forms import FormEditarUsuario
# importacion de las funcionalidaes
from plataform_CIGAP.utils.decoradores import grupo_usuario
from plataform_CIGAP.utils.funcionalidades_fechas import fecha_actual, fecha_maxima_respuesta


# Create your views here.

# vista de funcionamiento respecto a la url de la aplicacion
# def funcionando(request):
#     return HttpResponse('app_ estudiante funcionando.')

# recuperar anteproyecto por id
def recuperar_anteproyecto_id(id):
    anteproyecto = ModelAnteproyecto.objects.get(id=id)
    if not anteproyecto:
        return None
    return anteproyecto
# recuperacion de las observaciones de anteproyecto


def recuperar_observaciones_anteproyecto(anteproyecto):
    observaciones = ModelRetroalimentaciones.objects.filter(
        anteproyecto=anteproyecto)
    if not observaciones:
        return None
    return observaciones
# recuperacion de las observaciones de proyecto


def recuperar_observaciones_proyecto_final(proyecto):
    observaciones = ModelEvaluacionAnteproyecto.objects.filter(
        proyecto_final=proyecto)
    if not observaciones:
        return None
    return observaciones


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
        content_anteproyecto = ModelAnteproyecto.objects.get(
            user=request.user) if ModelAnteproyecto.objects.filter(user=request.user).exists() else None
        if content_anteproyecto == None:
            return None
        else:
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
    retroalimentaciones = ModelRetroalimentaciones.objects.filter(
        anteproyecto=anteproyecto_, estado__in=['Aprobado', 'Aprobado_con_correciones']).first() if ModelRetroalimentaciones.objects.filter(anteproyecto=anteproyecto_).exists() else None
    if retroalimentaciones:
        doc_convert = devolver_documento_imagen(
            retroalimentaciones.doc_retroalimentacion)
        return {'respuesta': retroalimentaciones,
                'doc_retroalimentacion': doc_convert}
    else:
        return None


def recuperar_retroalimentaciones(anteproyecto_):

    retroalimentaciones = ModelRetroalimentaciones.objects.filter(
        anteproyecto=anteproyecto_)
    respuestas = {}
    if retroalimentaciones.exists():
        for i, retroalimentacion in enumerate(retroalimentaciones):
            doc_convert = devolver_documento_imagen(
                retroalimentacion.doc_retroalimentacion)
            respuestas[f'retroalimentacion_{i}'] = {
                'respuesta': retroalimentacion,
                'doc_retroalimentacion': doc_convert
            }
    return respuestas if respuestas else None

# funcion parea recuperar el anteproyecto


def recuperar_anteproyecto(request):
    anteproyecto = ModelAnteproyecto.objects.get(
        Q(user=request.user) | Q(nombre_integrante1=request.user.nombre_completo) | Q(nombre_integrante1=request.user.nombre_completo))
    if not anteproyecto:
        return None
    return anteproyecto

# funcion para recuperar el proyecto final


def recuperar_proyecto_final(anteproyecto):
    proyecto_final = ModelProyectoFinal.objects.get(
        anteproyecto=anteproyecto) if ModelProyectoFinal.objects.filter(anteproyecto=anteproyecto).exists() else None
    return proyecto_final


@ login_required
@ grupo_usuario('Estudiantes')
def principal_estudiante(request):
    context = {}
    anteproyecto = recuperar_anteproyecto(request)
    retroalimentaciones = recuperar_retroalimentaciones(anteproyecto)
    if anteproyecto:
        context['anteproyecto'] = anteproyecto

    proyecto_final = recuperar_proyecto_final(anteproyecto)
    if proyecto_final:
        context['proyecto_final'] = proyecto_final
    if request.method == 'POST':
        editar_usuario(request)
    else:
        context = datosusuario(request)
        context['nombre_anteproyecto'] = anteproyecto.nombre_anteproyecto if anteproyecto else "No hay anteproyecto"
        context['retroalimentacion'] = retroalimentaciones

    return render(request, 'estudiante/base_estudiante.html', context)
# vista del template para la solicitud
#!funcionando


@ login_required
@ grupo_usuario('Estudiantes')
def solicitud(request):
    context = datosusuario(request)

    # Si el método es POST, procesamos el formulario.
    if request.method == 'POST':
        # Verificamos si el estudiante ya tiene un anteproyecto.
        try:
            # Buscamos un anteproyecto donde el usuario sea el creador o uno de los integrantes
            existing_anteproyecto = ModelAnteproyecto.objects.get(
                user=request.user)
            messages.warning(
                request, "Ya tienes un anteproyecto creado. No puedes crear otro hasta que el actual sea evaluado.")
            return redirect('estudiante:info_proyect')
        except ModelAnteproyecto.DoesNotExist:
            try:
                existing_anteproyecto1 = ModelAnteproyecto.objects.get(
                    nombre_integrante1=request.user.nombre_completo)
                messages.warning(
                    request, "Ya tienes un anteproyecto creado. No puedes crear otro hasta que el actual sea evaluado.")
                return redirect('estudiante:info_proyect')
            except ModelAnteproyecto.DoesNotExist:
                try:
                    existing_anteproyecto2 = ModelAnteproyecto.objects.get(
                        nombre_integrante2=request.user.nombre_completo)
                    messages.warning(
                        request, "Ya tienes un anteproyecto creado. No puedes crear otro hasta que el actual sea evaluado.")
                    return redirect('estudiante:info_proyect')
                except ModelAnteproyecto.DoesNotExist:
                    # Solo se ejecuta si no se encontró anteproyecto en ninguna de las condiciones anteriores
                    form = FormAnteproyecto(request.POST, request.FILES)
                    if form.is_valid():
                        anteproyecto = form.save(commit=False)
                        anteproyecto.estado = False
                        anteproyecto.user = request.user
                        anteproyecto.save()

                        # Mensaje de éxito
                        messages.success(
                            request, f"El proyecto '{anteproyecto.nombre_anteproyecto}' ha sido enviado al director y codirector para las retroalimentaciones pertinentes.")
                        return redirect('estudiante:info_proyect')
                    else:
                        # Mensaje de error si el formulario no es válido
                        messages.error(
                            request, "Hubo un problema al enviar el formulario. Por favor, verifica los campos y vuelve a intentarlo.")

    # Si el método es GET, buscamos el anteproyecto del usuario actual.
    else:
        try:
            anteproyecto = recuperar_anteproyecto(request)
            if anteproyecto:
                context['anteproyecto'] = anteproyecto
                if anteproyecto.fecha_envio:
                    context['fecha_respuesta_maxima'] = fecha_maxima_respuesta(
                        anteproyecto.fecha_envio)
                observaciones_anteproyecto = recuperar_observaciones_anteproyecto(
                    anteproyecto)
                if observaciones_anteproyecto:
                    dict_observaciones = {}
                    for i, observacion in enumerate(observaciones_anteproyecto):
                        # Crea un nuevo diccionario para cada observación
                        dict_observaciones[f'observacion{i}'] = {
                            'observacion': observacion,
                            'doc_evaluacion_anteproyecto': devolver_documento_imagen(observacion.doc_retroalimentacion)
                        }
                        context['observaciones'] = dict_observaciones
            proyecto_final = recuperar_proyecto_final(anteproyecto)
            content_anteproyecto = ModelAnteproyecto.objects.get(
                user=request.user)
        except ModelAnteproyecto.DoesNotExist:
            content_anteproyecto = None
            messages.warning(
                request, "No se encontró ningún anteproyecto asociado a tu cuenta.")

        if content_anteproyecto:
            estado = content_anteproyecto.solicitud_enviada
            existe_solicitud = content_anteproyecto.solicitud_enviada
            nombre_anteproyecto = content_anteproyecto.nombre_anteproyecto
            form_anteproyecto = FormAnteproyecto(instance=content_anteproyecto)
            context['form_anteproyecto'] = form_anteproyecto

            if existe_solicitud:
                context['existe_solicitud'] = existe_solicitud
                context['nombre_anteproyecto'] = nombre_anteproyecto
                context['fecha_envio'] = content_anteproyecto.fecha_envio
                messages.info(
                    request, f"La solicitud para el proyecto '{nombre_anteproyecto}' ya fue enviada anteriormente.")

        # lógica para saber si el proyecto fue aceptado
        context['respuesta'] = recuperar_retroalimentacion(
            content_anteproyecto)

        form_proyecto_final = FormProyectoFinal
        context['form_proyecto_final'] = form_proyecto_final
        form_solicitudes = FormSolicitudes
        context['form_solicitudes'] = form_solicitudes
        if proyecto_final:
            context['proyecto_final'] = proyecto_final

        return render(request, 'estudiante/solicitud.html', context)


def actualizar_documentos_anteproyecto(request, id):
    anteproyecto = recuperar_anteproyecto_id(id)

    if anteproyecto:
        if 'carta_anteproyecto' in request.FILES:
            anteproyecto.carta_presentacion = request.FILES.get(
                'carta_anteproyecto').read()
        if 'anteproyecto' in request.FILES:
            anteproyecto.anteproyecto = request.FILES.get(
                'anteproyecto').read()
            anteproyecto.save()
            messages.success(
                request, "El documento del anteproyecto se actualizó correctamente.")
        else:
            messages.warning(
                request, "No se encontró el archivo del anteproyecto para actualizar.")
    else:
        messages.error(
            request, "No se encontró el anteproyecto con el ID proporcionado.")

    return redirect('estudiante:solicitud')


# funcion de solicitudes especificas


def solicitudes_especificas(request):
    if request.method == 'POST':
        form = FormSolicitudes(request.POST, request.FILES)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.user = request.user
            solicitud.anteproyecto = recuperar_anteproyecto(request)
            solicitud.fecha_envio = fecha_actual()
            solicitud.estado = False
            solicitud.save()

            # Enviar mensaje de éxito
            messages.success(request, 'Solicitud enviada con éxito.')
            return redirect('estudiante:solicitud')
        else:
            # Enviar mensaje de error si el formulario no es válido
            messages.error(
                request, 'Error en el formulario. Por favor, revisa los datos ingresados.')
            return redirect('estudiante:solicitud')
    else:
        # Enviar mensaje de error si no es un POST
        messages.error(request, 'Método de solicitud no permitido.')
        return HttpResponse('Algo ocurrió.')

# vista de la informacion del proyecto


@login_required
@ grupo_usuario('Estudiantes')
def info_proyect(request):
    if request.method == 'POST':
        context = contenido_anteproyecto(request)

        return render(request, 'estudiante/Inf_proyect.html', context)
    else:
        context = contenido_anteproyecto(request)
        if context is None:
            context = {}
        anteproyecto = recuperar_anteproyecto(request)
        proyecto_final = recuperar_proyecto_final(anteproyecto)
        retroalimentaciones = recuperar_retroalimentaciones(anteproyecto)

        if proyecto_final:
            context['proyecto_final'] = proyecto_final
        if retroalimentaciones:
            # recordar que este recibe el documento y la respuesta general en un diccionario
            context['content_retroalimentacion'] = retroalimentaciones

            return render(request, 'estudiante/Inf_proyect.html', context)
        else:
            doc_revisado = None
            context['content_retroalimentacion'] = retroalimentaciones

            return render(request, 'estudiante/Inf_proyect.html', context)


@login_required
def enviar_solicitud_proyecto(request):
    print(f"Usuario autenticado: {request.user}")
    if request.method == 'POST':
        anteproyecto = recuperar_anteproyecto(request)

        print(f"Archivos subidos: {request.FILES}")

        form = FormProyectoFinal(request.POST, request.FILES)
        if form.is_valid():
            proyecto_final = form.save(commit=False)
            proyecto_final.user = request.user
            proyecto_final.anteproyecto = anteproyecto
            proyecto_final.descripcion = anteproyecto.descripcion
            proyecto_final.director = anteproyecto.director
            proyecto_final.estado = False
            proyecto_final.codirector = anteproyecto.codirector
            proyecto_final.solicitud_enviada = True
            proyecto_final.fecha_envio = fecha_actual()

            # Depuración: Verificar que los archivos aún estén presentes
            print(
                f"Archivo proyecto_final (longitud): {len(proyecto_final.proyecto_final) if proyecto_final.proyecto_final else 'No encontrado'}")
            print(
                f"Archivo carta_presentacion_final (longitud): {len(proyecto_final.carta_presentacion_final) if proyecto_final.carta_presentacion_final else 'No encontrado'}")

            # Guardar el proyecto final una sola vez
            proyecto_final.save()

            print(proyecto_final.codirector)
            print('Datos enviados correctamente')
            return redirect('estudiante:solicitud')
        else:
            print(f"Errores del formulario: {form.errors}")

    return redirect('estudiante:solicitud')
