from django.shortcuts import render
from django.utils import timezone
from apps.accounts.decorators import rol_requerido
from apps.accounts.models import User
from apps.doctor.models import PerfilDoctor, Receta
from apps.paciente.models import PerfilPaciente
from .models import Bitacora


@rol_requerido('ADMIN')
def inicio(request):
    return render(request, 'administrador/inicio.html', {
        'total_usuarios': User.objects.count(),
        'total_doctores': PerfilDoctor.objects.count(),
        'total_pacientes': PerfilPaciente.objects.count(),
        'total_recetas': Receta.objects.count(),
        'accesos_hoy': Bitacora.objects.filter(
            accion='LOGIN', fecha__date=timezone.localdate()
        ).count(),
        'doctores': PerfilDoctor.objects.select_related('usuario'),
        'pacientes': PerfilPaciente.objects.select_related('usuario'),
        'recetas': Receta.objects.select_related('paciente__usuario', 'doctor__usuario')[:20],
        'bitacora': Bitacora.objects.select_related('usuario')[:15],
    })