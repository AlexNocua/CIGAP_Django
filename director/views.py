from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required
from plataform_CIGAP.decoradores import grupo_usuario
# Create your views here.


# def funcionando(request):
#     return HttpResponse('app_ director funcionando.')

@login_required
@grupo_usuario('Directores')
def base_director(request):
    return render(request, 'director/base_director.html')
