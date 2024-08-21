import django.contrib.auth
from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from plataform_CIGAP.views import logout_user
from django.contrib.auth.decorators import login_required
from plataform_CIGAP.decoradores import grupo_usuario

# Create your views here.
# def funcionando (request):
#     return HttpResponse('app_ correspondencia funcionando.')


@login_required
@grupo_usuario('Correspondencia')
def principal_correspondencia(request):
    return render(request, 'correspondencia/base_correspondencia.html')
