from django.shortcuts import render
from apps.accounts.decorators import rol_requerido
from apps.doctor.models import DoctorPaciente, Receta


@rol_requerido('PACIENTE')
def inicio(request):
    perfil = getattr(request.user, 'perfil_paciente', None)
    if perfil is None:
        return render(request, 'paciente/inicio.html', {'sin_perfil': True})

    recetas = (
        Receta.objects.filter(paciente=perfil)
        .select_related('doctor__usuario')
        .prefetch_related('detalles')
    )
    doctores = (
        DoctorPaciente.objects.filter(paciente=perfil)
        .select_related('doctor__usuario')
        .order_by('-activo', '-fecha_inicio')
    )
    return render(request, 'paciente/inicio.html', {
        'perfil': perfil,
        'recetas': recetas,
        'doctores': doctores,
        'total_doctores': doctores.filter(activo=True).count(),
        'total_recetas': recetas.count(),
        'recetas_vigentes': recetas.filter(estado=Receta.Estado.VIGENTE).count(),
    })