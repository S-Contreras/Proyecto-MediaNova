from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def redirigir_por_rol(request):
    destinos = {
        'ADMIN': 'administrador:inicio',
        'DOCTOR': 'doctor:inicio',
        'PACIENTE': 'paciente:inicio',
    }
    return redirect(destinos[request.user.rol])