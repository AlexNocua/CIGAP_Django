# Asegúrate de que la ruta de importación sea correcta
from django.conf import settings
import requests
from .models import Usuarios  # Asegúrate de importar tu modelo Usuarios
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .forms import FormRegistro
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

import re
# Create your views here.


from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# importacion de los models


from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import HttpResponse

from .forms import FormRegistro, FormEditarUsuario


# importacion para la codificacion de las imagenes
import base64

# importacion de modelo de usuarios
from .models import Usuarios


# utilidades
def existe_usuario(email):
    usuario = Usuarios.objects.get(email=email) if Usuarios.objects.filter(
        email=email).exists() else None
    if not usuario:
        return None
    return True


# Creacion de la vista global del login
def loginapps(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Username: {username}, Password: {password}")
        user = authenticate(request, username=username, password=password)
        print(f"Authenticated User: {user}")

        if user is not None:
            print("User is authenticated")
            auth_login(request, user)
            user_groups = user.groups.values_list('name', flat=True)
            print(f"User Groups: {user_groups}")
            if 'Estudiantes' in user_groups:
                return redirect('estudiante:principal_estudiante')
            elif 'Directores' in user_groups:
                return redirect('director:principal_director')
            elif 'Correspondencia' in user_groups:
                return redirect('correspondencia:principal_correspondencia')
            else:
                return HttpResponse("No tienes acceso a ninguna sección.")
        else:
            return HttpResponse("Credenciales inválidas")

    else:
        form = FormRegistro
        return render(request, "login.html", {'form': form})


def registro(request):
    if request.method == 'POST':
        form = FormRegistro(request.POST)
        email = form.data.get('email')
        existe = existe_usuario(email)

        if existe:
            messages.error(
                request, f"Error en el registro. El correo electrónico {email} ya se encuentra registrado.")
            return redirect('login:loginapps')

        if form.is_valid():
            user = form.save()
            messages.success(
                request, f"El usuario {user.email} ha sido registrado exitosamente.")
            return redirect('login:loginapps')
        else:

            password1_errors = form.errors.get('password1', [])
            password2_errors = form.errors.get('password2', [])
            if password1_errors:
                messages.error(
                    request, f"Error en el registro. {' '.join(password1_errors)}")
            if password2_errors:
                messages.error(
                    request, f"Error en el registro. {' '.join(password2_errors)}")
            return redirect('login:loginapps')
    else:
        return redirect('login:loginapps')


# esta es la funcion que permite cambiar los datos de cada uno de los estudiantes
def editar_usuario(request):
    usuario = request.user
    # recuperacion de la imagen propia del usuaario en formato binario
    # print(imagen, 'esta es la imagen')
    imagen = usuario.imagen
    imagen_convertida = base64.b64encode(
        imagen).decode('utf-8') if imagen else ''

    if request.method == 'POST':
        form = FormEditarUsuario(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            user = form.save()

            # revizar esta logica
            # Autenticar de nuevo al usuario si el correo electrónico ha cambiado
            if user.email != request.user.email:
                auth_login(request, user)
            user_groups = user.groups.values_list('name', flat=True)
            if 'Estudiantes' in user_groups:
                return redirect('estudiante:principal_estudiante')
            elif 'Directores' in user_groups:
                return redirect('director:principal_director')
            elif 'Correspondencia' in user_groups:
                return redirect('correspondencia:principal_correspondencia')
            else:
                return HttpResponse("No tienes acceso a ninguna seción")
            return redirect('director:base_director')
        else:
            return render(request, 'director/base_director.html', {'form_config': form, 'usuario': usuario, 'user_img': imagen_convertida})


def recuperar_cuenta(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = Usuarios.objects.get(email=email)  # Usa tu modelo Usuarios
            token = get_random_string(length=32)  # Generar un token único
            user.token = token  # Asigna el token al usuario
            user.save()  # Guarda el usuario con el token

            # Crear el enlace de recuperación
            recovery_link = request.build_absolute_uri(
                reverse('login:recuperar_cuenta_confirm', args=[token]))

            # Intentar enviar el correo electrónico usando Resend
            try:
                response = requests.post(
                    'https://api.resend.com/emails',
                    headers={
                        'Authorization': f'Bearer {settings.RESEND_API_KEY}',
                        'Content-Type': 'application/json',
                    },
                    json={
                        'from': settings.EMAIL_FROM,
                        'to': [email],
                        'subject': 'Recuperación de cuenta',
                        'html': f'<p>Haz clic en el siguiente enlace para recuperar tu cuenta: <a href="{recovery_link}">{recovery_link}</a></p>',
                    }
                )

                if response.status_code == 200:
                    messages.success(
                        request, 'Se ha enviado un enlace de recuperación a tu correo electrónico.')
                else:
                    messages.error(
                        request, f'Error al enviar el correo: {response.text}.')

                return redirect('login:loginapps')

            except Exception as e:  # Captura cualquier excepción al hacer la solicitud
                messages.error(
                    request, f'Hubo un error al enviar el correo de recuperación: {str(e)}. Por favor, intenta nuevamente.')
                return render(request, 'recuperar_cuenta.html')

        except Usuarios.DoesNotExist:  # Cambiar User por Usuarios
            messages.error(
                request, 'No existe un usuario con ese correo electrónico.')

    return render(request, 'recuperar_cuenta.html')


def recuperar_cuenta_confirm(request, token):
    # Aquí deberías validar el token y permitir que el usuario restablezca su contraseña
    # Esto es solo un ejemplo de cómo podrías manejarlo
    if request.method == 'POST':
        nueva_contrasena = request.POST.get('nueva_contrasena')
        # Aquí deberías implementar la lógica para encontrar al usuario por el token
        # y actualizar su contraseña

        # Suponiendo que encuentras al usuario:
        try:
            # Asegúrate de tener el token guardado en el modelo
            user = Usuarios.objects.get(token=token)
            user.set_password(nueva_contrasena)  # Establecer nueva contraseña
            user.save()  # Guardar el usuario
            messages.success(request, 'Tu contraseña ha sido actualizada.')
            # Redirigir a la página de inicio de sesión
            return redirect('login:loginapps')
        except Usuarios.DoesNotExist:
            messages.error(request, 'El token de recuperación es inválido.')

    return render(request, 'recuperar_cuenta_confirm.html', {'token': token})
