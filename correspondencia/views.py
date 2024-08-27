import django.contrib.auth
from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from plataform_CIGAP.views import logout_user
from django.contrib.auth.decorators import login_required
# importacion de las funcionalidaes
from plataform_CIGAP.utils.decoradores import grupo_usuario
from plataform_CIGAP.utils.funcionalidades_fechas import fecha_actual


# Create your views here.
# def funcionando (request):
#     return HttpResponse('app_ correspondencia funcionando.')


@login_required
@grupo_usuario('Correspondencia')
def principal_correspondencia(request):
    return render(request, 'correspondencia/base_correspondencia.html')
