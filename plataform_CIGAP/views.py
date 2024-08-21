from django.shortcuts import redirect
# unica importacion para manejar el LogOut de las cuentas
from django.contrib.auth import logout 

def logout_user(request):
    logout(request)
    return redirect('login:loginapps')