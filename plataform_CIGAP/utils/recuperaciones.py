# importaciones de funcionalidades
from django.db.models import Q
import base64
from login.forms import FormEditarUsuario

# importaciones de los modelos de cada una de las aplicaciones
from estudiante.models import (
    ModelFechasProyecto,
    ModelProyectoFinal,
    ModelAsignacionJurados,
    ModelAnteproyecto,
)
from director.models import *
from correspondencia.models import (
    ModelDocumentos,
    ModelSolicitudes,
    ModelInformacionEntregaFinal,
    ModelRetroalimentaciones,
    ModelDocumentos,
)
from django.contrib.auth.decorators import login_required

# funcion de recuperar documento binario


@login_required
def datosusuario(request):

    usuario = request.user
    imagen = usuario.imagen
    imagen_convertida = base64.b64encode(imagen).decode("utf-8") if imagen else ""
    form_editar_usuario = FormEditarUsuario(instance=usuario)

    context = {
        "form_config": form_editar_usuario,
        "usuario": usuario,
        "user_img": imagen_convertida,
    }
    return context


def recuperar_documento(documento):
    documento = base64.b64encode(documento).decode("utf-8") if documento else None
    return documento


def recuperar_num_respuestas():
    num_respuestas = ModelRetroalimentaciones.objects.all().count()
    return num_respuestas


def recuperar_num_proyectos_terminados():
    num_proyectos = ModelProyectoFinal.objects.filter(estado=True).count()
    return num_proyectos


def recuperar_num_proyectos_pendientes():
    num_proyectos_pendientes = ModelAnteproyecto.objects.filter(estado=True).count()
    return num_proyectos_pendientes


def recuperar_num_solicitudes():
    num_solicitudes = ModelSolicitudes.objects.filter(estado=False).count()
    num_anteproyectos = ModelAnteproyecto.objects.filter(
        Q(solicitud_enviada=True) & Q(estado=False)
    ).count()
    num_proyectos_finales = ModelProyectoFinal.objects.filter(
        Q(solicitud_enviada=True) & Q(estado=False)
    ).count()
    print(num_solicitudes)
    print(num_anteproyectos)
    print(num_proyectos_finales)
    suma = num_solicitudes + num_anteproyectos + num_proyectos_finales
    return suma


def recuperar_num_formatos_comite():
    num_formatos = ModelDocumentos.objects.all().count()
    return num_formatos


#######################################################################################################

# revisar


def recuperar_proyectos_pendientes():

    proyectos_finales = ModelProyectoFinal.objects.filter(
        Q(Q(solicitud_enviada=False) & Q(estado=False))
        | Q(Q(solicitud_enviada=True) & Q(estado=False))
    )
    if proyectos_finales:
        return proyectos_finales
    else:
        return None


def recuperar_proyectos_finalizados():
    proyectos_finalizados = ModelProyectoFinal.objects.filter(
        Q(solicitud_enviada=True) & Q(estado=True)
    )
    if not proyectos_finalizados:
        proyectos_finalizados = None
    return proyectos_finalizados


def recuperar_proyecto_finalizado(id):
    proyecto = (
        ModelProyectoFinal.objects.get(id=id)
        if ModelProyectoFinal.objects.filter(id=id).exists()
        else None
    )
    return proyecto


def recuperar_proyecto_actual(id):
    proyecto = (
        ModelProyectoFinal.objects.get(id=id)
        if ModelProyectoFinal.objects.filter(id=id).exists()
        else None
    )
    return proyecto


def recuperar_solicitudes_especiales_proyecto(proyecto, anteproyecto):
    solicitudes_especiales_proyecto = ModelSolicitudes.objects.filter(
        Q(proyecto_final=proyecto) | Q(anteproyecto=anteproyecto)
    )
    print(solicitudes_especiales_proyecto.count())
    return solicitudes_especiales_proyecto


def recuperar_fechas_proyecto(proyecto):
    fechas = (
        ModelFechasProyecto.objects.get(proyecto_final=proyecto)
        if ModelFechasProyecto.objects.filter(proyecto_final=proyecto).exists()
        else None
    )
    return fechas


#######################################################################################################
# recuperacion de los documentos cargados por el comite


def recuperar_formatos():
    documentos_model = ModelDocumentos.objects.all()
    documentos = {}
    if documentos_model:
        for i, documento in enumerate(documentos_model):
            documento_binario = documento.documento
            documento_convert = recuperar_documento(documento_binario)
            documentos[f"documento{i}"] = {
                "id": documento.id,
                "nombre_documento": documento.nombre_documento,
                "descripcion": documento.descripcion,
                "version": documento.version,
                "documento": documento_convert,
                "fecha_cargue": documento.fecha_cargue,
            }
    else:
        documentos = None

    return documentos
