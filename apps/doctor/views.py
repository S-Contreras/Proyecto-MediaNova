from django.shortcuts import render
from apps.accounts.decorators import rol_requerido
from .models import DoctorPaciente, Receta


@rol_requerido('DOCTOR')
def inicio(request):
    perfil = getattr(request.user, 'perfil_doctor', None)
    if perfil is None:
        return render(request, 'doctor/inicio.html', {'sin_perfil': True})

    asignaciones = (
        DoctorPaciente.objects.filter(doctor=perfil, activo=True)
        .select_related('paciente__usuario')
    )
    todas_recetas = Receta.objects.filter(doctor=perfil)
    recetas = (
        todas_recetas
        .select_related('paciente__usuario')
        .prefetch_related('detalles')[:20]
    )
    return render(request, 'doctor/inicio.html', {
        'perfil': perfil,
        'asignaciones': asignaciones,
        'recetas': recetas,
        'total_pacientes': asignaciones.count(),
        'total_recetas': todas_recetas.count(),
        'recetas_vigentes': todas_recetas.filter(estado=Receta.Estado.VIGENTE).count(),
    })