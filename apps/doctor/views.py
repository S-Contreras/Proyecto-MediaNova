import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from apps.accounts.decorators import rol_requerido
from apps.administrador.models import Bitacora
from apps.doctor.models import DetalleReceta, DoctorPaciente, PerfilDoctor, Receta
from apps.paciente.models import PerfilPaciente


@login_required
@rol_requerido('DOCTOR')
def inicio(request):
    doctor = PerfilDoctor.objects.filter(usuario=request.user).first()

    if not doctor:
        return render(
            request,
            'doctor/inicio.html',
            {
                'sin_perfil': True,
                'doctor': None,
                'asignaciones': [],
                'recetas': [],
                'recetas_historial': [],
                'total_pacientes': 0,
                'total_recetas': 0,
                'recetas_vigentes': 0,
            },
        )

    asignaciones = (
        DoctorPaciente.objects.filter(doctor=doctor, activo=True)
        .select_related('paciente__usuario')
        .order_by('-fecha_inicio')
    )
    pacientes_asignados = [a.paciente for a in asignaciones]

    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'emitir_receta':
            paciente_id = request.POST.get('paciente_id')
            diagnostico = request.POST.get('diagnostico', '').strip()
            indicaciones = request.POST.get('indicaciones', '').strip()
            medicamento = request.POST.get('medicamento', '').strip()
            dosis = request.POST.get('dosis', '').strip()
            frecuencia = request.POST.get('frecuencia', '').strip()
            duracion = request.POST.get('duracion', '').strip()

            paciente = PerfilPaciente.objects.filter(id=paciente_id).first()
            if not paciente or not any(p.id == paciente.id for p in pacientes_asignados):
                messages.error(request, 'Selecciona un paciente asignado válido.')
                return redirect('doctor:inicio')

            if not diagnostico:
                messages.error(request, 'El diagnóstico es obligatorio para emitir la receta.')
                return redirect('doctor:inicio')

            with transaction.atomic():
                folio = f"RX-{uuid.uuid4().hex[:8].upper()}"
                receta = Receta.objects.create(
                    folio=folio,
                    paciente=paciente,
                    doctor=doctor,
                    diagnostico=diagnostico,
                    indicaciones=indicaciones,
                    estado='EMITIDA',
                )
                if medicamento:
                    DetalleReceta.objects.create(
                        receta=receta,
                        medicamento=medicamento,
                        dosis=dosis or 'Según indicación',
                        frecuencia=frecuencia or 'Según indicación',
                        duracion=duracion or 'Según indicación',
                    )

                Bitacora.objects.create(
                    usuario=request.user,
                    accion='CREAR_RECETA',
                    entidad='Receta',
                    objeto_id=str(receta.pk),
                )

            messages.success(request, f'Receta {folio} emitida correctamente.')
            return redirect('doctor:inicio')

        elif accion == 'editar_receta':
            receta_id = request.POST.get('receta_id')
            diagnostico = request.POST.get('diagnostico', '').strip()
            indicaciones = request.POST.get('indicaciones', '').strip()

            receta = Receta.objects.filter(id=receta_id, doctor=doctor).first()
            if not receta:
                messages.error(request, 'No se encontró la receta indicada.')
                return redirect('doctor:inicio')

            if not diagnostico:
                messages.error(request, 'El diagnóstico no puede quedar vacío.')
                return redirect('doctor:inicio')

            receta.diagnostico = diagnostico
            receta.indicaciones = indicaciones
            receta.save(update_fields=['diagnostico', 'indicaciones'])

            Bitacora.objects.create(
                usuario=request.user,
                accion='EDIT_RECETA',
                entidad='Receta',
                objeto_id=str(receta.pk),
            )
            messages.success(request, f'Receta {receta.folio} actualizada.')
            return redirect('doctor:inicio')

        elif accion == 'cancelar_receta':
            receta_id = request.POST.get('receta_id')
            receta = Receta.objects.filter(id=receta_id, doctor=doctor).first()
            if not receta:
                messages.error(request, 'No se encontró la receta indicada.')
                return redirect('doctor:inicio')

            receta.estado = 'CANCELADA'
            receta.save(update_fields=['estado'])

            Bitacora.objects.create(
                usuario=request.user,
                accion='CANC_RECETA',
                entidad='Receta',
                objeto_id=str(receta.pk),
            )
            messages.success(request, f'Receta {receta.folio} cancelada.')
            return redirect('doctor:inicio')

    recetas = (
        Receta.objects.filter(doctor=doctor)
        .select_related('paciente__usuario')
        .prefetch_related('detalles')
        .order_by('-fecha_emision')[:25]
    )

    recetas_historial = (
        Receta.objects.filter(paciente__doctores__doctor=doctor, paciente__doctores__activo=True)
        .select_related('paciente__usuario', 'doctor__usuario')
        .prefetch_related('detalles')
        .distinct()
        .order_by('-fecha_emision')
    )

    total_recetas = Receta.objects.filter(doctor=doctor).count()
    recetas_vigentes = Receta.objects.filter(doctor=doctor, estado__iexact='emitida').count()

    return render(
        request,
        'doctor/inicio.html',
        {
            'sin_perfil': False,
            'doctor': doctor,
            'asignaciones': asignaciones,
            'recetas': recetas,
            'recetas_historial': recetas_historial,
            'total_pacientes': asignaciones.count(),
            'total_recetas': total_recetas,
            'recetas_vigentes': recetas_vigentes,
        },
    )