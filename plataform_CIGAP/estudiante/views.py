from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect

# Create your views here.


def funcionando(request):
    return HttpResponse('app_ estudiante funcionando.')


def principal(request):
    return render(request, 'estudiante/base_estudiante.html')


def estudiante(request):
    return render(request, 'estudiante/estudiante.html')
