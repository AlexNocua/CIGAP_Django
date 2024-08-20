from django.shortcuts import render

# Create your views here.


from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# importacion de los models
from estudiante.models import Estudiante

from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import HttpResponse

from .forms import FormRegistro


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
                return redirect('director:base_director')
            elif 'Correspondencia' in user_groups:
                return redirect('correspondencia_home')
            else:
                return HttpResponse("No tienes acceso a ninguna sección.")
        else:
            return HttpResponse("Credenciales inválidas")

    else:
        form = FormRegistro
        return render(request, "login.html", {'form': form})


def registro(request):
    # # ejemplo de uso de mensajes
    # messages.success(request, 'Operación exitosa.')

    # # Agregar un mensaje de error
    # messages.error(request, 'Hubo un error en la operación.')

    # # Agregar un mensaje de advertencia
    # messages.warning(request, 'Advertencia: Verifica los detalles.')

    # # Agregar un mensaje informativo
    # messages.info(request, 'Información: Revisa la sección de ayuda.')

    if request.method == 'POST':
        form = FormRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            # insercion de mensajes
            messages.success(request, "Registro good")
            return redirect('login:loginapps')
        else:
            messages.error(request, "Error en el registro")
            return redirect('login:loginapps')
    else:
        return redirect('login:loginapps')
