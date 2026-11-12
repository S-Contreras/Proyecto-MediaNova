from django.shortcuts import render
from apps.accounts.decorators import rol_requerido


@rol_requerido('ADMIN')
def inicio(request):
    return render(request, 'administrador/inicio.html')