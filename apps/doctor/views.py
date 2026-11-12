from django.shortcuts import render
from apps.accounts.decorators import rol_requerido


@rol_requerido('DOCTOR')
def inicio(request):
    return render(request, 'doctor/inicio.html')