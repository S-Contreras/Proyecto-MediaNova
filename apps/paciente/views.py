from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.accounts.decorators import rol_requerido
from apps.administrador.models import Bitacora
from apps.doctor.models import DoctorPaciente, Receta
from apps.paciente.models import PerfilPaciente


@login_required
@rol_requerido('PACIENTE')
def inicio(request):
    perfil = PerfilPaciente.objects.filter(usuario=request.user).first()

    if not perfil:
        return render(
            request,
            'paciente/inicio.html',
            {
                'sin_perfil': True,
                'perfil': None,
                'doctores': [],
                'recetas': [],
                'total_doctores': 0,
                'recetas_vigentes': 0,
                'total_recetas': 0,
            },
        )

    if request.method == 'POST' and request.POST.get('accion') == 'actualizar_contacto':
        telefono = request.POST.get('telefono', '').strip()
        email = request.POST.get('email', '').strip()

        if hasattr(request.user, 'telefono'):
            request.user.telefono = telefono
        if email:
            request.user.email = email
        request.user.save()

        Bitacora.objects.create(
            usuario=request.user,
            accion='EDIT_CONTACTO',
            entidad='PerfilPaciente',
            objeto_id=str(perfil.pk),
        )

        messages.success(request, 'Tus datos de contacto se actualizaron correctamente.')
        return redirect('paciente:inicio')

    doctores = (
        DoctorPaciente.objects.filter(paciente=perfil)
        .select_related('doctor__usuario')
        .order_by('-activo', '-fecha_inicio')
    )

    recetas = (
        Receta.objects.filter(paciente=perfil)
        .select_related('doctor__usuario')
        .prefetch_related('detalles')
        .order_by('-fecha_emision')
    )

    total_recetas = recetas.count()
    recetas_vigentes = recetas.filter(estado__iexact='emitida').count()

    return render(
        request,
        'paciente/inicio.html',
        {
            'sin_perfil': False,
            'perfil': perfil,
            'doctores': doctores,
            'recetas': recetas,
            'total_doctores': doctores.count(),
            'recetas_vigentes': recetas_vigentes,
            'total_recetas': total_recetas,
        },
    )