from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect


# Creacion de la vista global del login
def login(request):
    return render(request, "login.html")
