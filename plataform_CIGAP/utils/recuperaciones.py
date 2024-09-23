# importaciones de funcionalidades
from django.db.models import Q

# importaciones de los modelos de cada una de las aplicaciones
from estudiante.models import ModelProyectoFinal, ModelAsignacionJurados, ModelAnteproyecto
from director.models import *
from correspondencia.models import ModelDocumentos, ModelSolicitudes, ModelInformacionEntregaFinal, ModelRetroalimentaciones


def recuperar_num_respuestas():
    num_respuestas = ModelRetroalimentaciones.objects.all().count()
    return num_respuestas


def recuperar_num_proyectos_terminados():
    num_proyectos = ModelProyectoFinal.objects.filter(estado=True).count()
    return num_proyectos


def recuperar_num_proyectos_pendientes():
    num_proyectos_pendientes = ModelAnteproyecto.objects.filter(
        estado=True).count()
    return num_proyectos_pendientes


def recuperar_num_solicitudes():
    num_solicitudes = ModelSolicitudes.objects.filter(
        estado=False).count()
    num_anteproyectos = ModelAnteproyecto.objects.filter(
        Q(solicitud_enviada=True) & Q(estado=False)).count()
    num_proyectos_finales = ModelProyectoFinal.objects.filter(
        Q(solicitud_enviada=True) & Q(estado=False)).count()
    print(num_solicitudes)
    print(num_anteproyectos)
    print(num_proyectos_finales)
    suma = num_solicitudes + num_anteproyectos + num_proyectos_finales
    return suma


def recuperar_num_formatos_comite():
    num_formatos = ModelDocumentos.objects.all().count()
    return num_formatos

#######################################################################################################


def recuperar_proyectos_pendientes():
    proyectos_pendientes = ModelAnteproyecto.objects.filter(
        Q(solicitud_enviada=True) & Q(estado=True))
    print(proyectos_pendientes, 'Desde utilidades')
    if proyectos_pendientes:
        return proyectos_pendientes
    else:
        proyectos_pendientes = None
        return proyectos_pendientes


def recuperar_proyectos_finalizados():
    proyectos_finalizados = ModelProyectoFinal.objects.filter(
        Q(solicitud_enviada=True) & Q(estado=True))
    if not proyectos_finalizados:
        proyectos_finalizados = None
    return proyectos_finalizados


def recuperar_proyecto_finalizado(id):
    proyecto = ModelProyectoFinal.objects.get(
        id=id) if ModelProyectoFinal.objects.filter(id=id).exists() else None
    return proyecto


def recuperar_proyecto_actual(id):
    proyecto = ModelAnteproyecto.objects.get(
        id=id) if ModelAnteproyecto.objects.filter(id=id).exists() else None
    return proyecto
#######################################################################################################
