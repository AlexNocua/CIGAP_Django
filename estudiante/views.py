from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from .forms import FormPrimeraSolicitud
from django.contrib.auth.decorators import login_required

# Create your views here.

# vista de funcionamiento respecto a la url de la aplicacion
# def funcionando(request):
#     return HttpResponse('app_ estudiante funcionando.')





@login_required
def principal_estudiante(request):
    return render(request, 'estudiante/base_estudiante.html')

# vista del template para la solicitud


#!funcionando
@login_required
def solicitud(request):
    if request.method == 'POST':
        form = FormPrimeraSolicitud(request.POST)
        if form.is_valid():
            form.save()
        return redirect('estudiante:solicitud')
    else:
        form = FormPrimeraSolicitud
        context = {'form': form}
        return render(request, 'estudiante/template_solicitud.html', context)


# def estudiante(request):
#     return render(request, 'estudiante/estudiante.html')
