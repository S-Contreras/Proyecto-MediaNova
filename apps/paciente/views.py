from django.shortcuts import render
from apps.accounts.decorators import rol_requerido


@rol_requerido('PACIENTE')
def inicio(request):
    return render(request, 'paciente/inicio.html')