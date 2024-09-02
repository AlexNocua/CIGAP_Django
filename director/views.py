from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required
from login.models import Usuarios
from django.contrib.auth import login as auth_login
import base64
# importacion de las funcionalidaes
from plataform_CIGAP.utils.decoradores import grupo_usuario
from plataform_CIGAP.utils.funcionalidades_fechas import fecha_actual

# importacion de la vista del login que permite cambiar la informacion de ususario
from login.views import editar_usuario
from login.forms import FormEditarUsuario
# Create your views here.


# def funcionando(request):
#     return HttpResponse('app_ director funcionando.')

@login_required
@grupo_usuario('Directores')
def principal_director(request):
    usuario = request.user
    # recuperacion de la imagen propia del usuaario en formato binario
    # print(imagen, 'esta es la imagen')
    imagen = usuario.imagen
    imagen_convertida = base64.b64encode(
        imagen).decode('utf-8') if imagen else ''

    if request.method == 'POST':
        editar_usuario(request)
    else:
        form = FormEditarUsuario(instance=usuario)
        return render(request, 'director/base_director.html', {'form_config': form, 'usuario': usuario, 'user_img': imagen_convertida})

# def base_director(request):
#     usuario = request.user
#     # recuperacion de la imagen propia del usuaario en formato binario
#     # print(imagen, 'esta es la imagen')
#     imagen = usuario.imagen
#     imagen_convertida = base64.b64encode(imagen).decode('utf-8') if imagen else ''

#     if request.method == 'POST':
#         form = FormEditarUsuario(request.POST, request.FILES, instance=usuario)
#         if form.is_valid():
#             user = form.save()

#             # revizar esta logica
#             # Autenticar de nuevo al usuario si el correo electrónico ha cambiado
#             if user.email != request.user.email:
#                 auth_login(request, user)
#             return redirect('director:base_director')
#         else:
#             return render(request, 'director/base_director.html', {'form_config': form, 'usuario': usuario, 'user_img':imagen_convertida })
#     else:
#         form = FormEditarUsuario(instance=usuario)
#         return render(request, 'director/base_director.html', {'form_config': form, 'usuario': usuario, 'user_img':imagen_convertida })
