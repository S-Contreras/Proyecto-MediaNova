from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Consentimiento, User


@login_required
def redirigir_por_rol(request):
    rol_normalizado = (request.user.rol or '').upper()

    if rol_normalizado == User.Rol.PACIENTE:
        tiene_consentimiento = Consentimiento.objects.filter(
            usuario=request.user,
            version_aviso=settings.AVISO_VERSION,
            datos_salud=True,
        ).exists()
        if not tiene_consentimiento:
            return redirect('consentimiento')

    rutas_por_rol = {
        User.Rol.ADMIN: 'administrador:inicio',
        User.Rol.DOCTOR: 'doctor:inicio',
        User.Rol.PACIENTE: 'paciente:inicio',
    }
    destino = rutas_por_rol.get(rol_normalizado, 'login')
    return redirect(destino)


def aviso_privacidad(request):
    return render(request, 'accounts/aviso_privacidad.html')


@login_required
def consentimiento(request):
    if request.method == 'POST':
        if request.POST.get('datos_salud') != 'on':
            return render(request, 'accounts/consentimiento.html', {
                'error': 'Para usar el sistema debe aceptar el tratamiento de sus datos de salud.'
            })
        Consentimiento.objects.create(
            usuario=request.user,
            version_aviso=settings.AVISO_VERSION,
            datos_salud=True,
            asistente_expediente=request.POST.get('asistente_expediente') == 'on',
            estadisticas=request.POST.get('estadisticas') == 'on',
            ip=request.META.get('REMOTE_ADDR'),
        )
        return redirect('redirigir_por_rol')
    return render(request, 'accounts/consentimiento.html')