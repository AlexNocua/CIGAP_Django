from django.shortcuts import redirect
from django.http import HttpResponse

# Es este script vamos a crear un decroador el cual va a poner un filtro de usuarios que inician secion.
# esto con el fin de controlar el acceso a otras aplicaciones por medio de las url, estas solo por permiciones de grupos


def grupo_usuario(nombre_grupo):
    def decorador(view):
        def view_envuelta(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.groups.filter(name=nombre_grupo).exists():
                    return view(request, *args, **kwargs)
                else:
                    
                    # en este decorador puedo manejar una vista de permisos
                    return HttpResponse('Error')
                    

            else:
                
                return HttpResponse('Error, el usuario no esta autenticado.')
                # return redirect
        return view_envuelta
    return decorador
