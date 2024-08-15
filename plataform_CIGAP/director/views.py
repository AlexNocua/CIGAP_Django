from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect


# Create your views here.


# def funcionando(request):
#     return HttpResponse('app_ director funcionando.')


def principal_director(request):
    return render(request, 'director/principal_director.html')
