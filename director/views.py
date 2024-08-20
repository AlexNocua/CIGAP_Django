from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.


# def funcionando(request):
#     return HttpResponse('app_ director funcionando.')

@login_required
def base_director(request):
    return render(request, 'director/base_director.html')
