from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import ProtectedError

from apps.accounts.decorators import rol_requerido
from apps.administrador.models import Bitacora
from apps.doctor.models import DoctorPaciente, PerfilDoctor, Receta
from apps.paciente.models import PerfilPaciente

User = get_user_model()


@login_required
@rol_requerido(User.Rol.ADMIN)
def inicio(request):
    if request.method == 'POST':
        accion = request.POST.get('accion', '').strip()

        if accion == 'crear_usuario':
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            rol = request.POST.get('rol', User.Rol.PACIENTE).strip().upper()
            email = request.POST.get('email', '').strip()
            telefono = request.POST.get('telefono', '').strip()
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            apellido_materno = request.POST.get('apellido_materno', '').strip()

            if not username or not password:
                messages.error(request, 'Debes ingresar usuario y contraseña.')
                return redirect('administrador:inicio')

            if User.objects.filter(username=username).exists():
                messages.error(request, f'El usuario "{username}" ya existe.')
                return redirect('administrador:inicio')

            nuevo_usuario = User.objects.create_user(
                username=username,
                password=password,
                rol=rol,
                email=email,
                telefono=telefono,
                first_name=first_name,
                last_name=last_name,
                apellido_materno=apellido_materno,
            )

            if rol == User.Rol.DOCTOR:
                PerfilDoctor.objects.create(
                    usuario=nuevo_usuario,
                    cedula_profesional=request.POST.get('cedula_profesional', '').strip(),
                    especialidad=request.POST.get('especialidad', '').strip(),
                )
            elif rol == User.Rol.PACIENTE:
                fecha_nac_raw = request.POST.get('fecha_nacimiento', '').strip()
                perfil_pac = PerfilPaciente.objects.create(
                    usuario=nuevo_usuario,
                    curp=request.POST.get('curp', '').strip().upper(),
                    fecha_nacimiento=fecha_nac_raw or None,
                    sexo=request.POST.get('sexo', '').strip(),
                    tipo_sangre=request.POST.get('tipo_sangre', '').strip(),
                    alergias=request.POST.get('alergias', '').strip(),
                    padecimientos=request.POST.get('padecimientos', '').strip(),
                )

                doctor_id = request.POST.get('doctor_id', '').strip()
                if doctor_id:
                    doc_perfil = PerfilDoctor.objects.filter(id=doctor_id).first()
                    if doc_perfil:
                        DoctorPaciente.objects.create(
                            doctor=doc_perfil,
                            paciente=perfil_pac,
                            fecha_inicio=timezone.localdate(),
                            activo=True,
                        )
            elif rol == User.Rol.ADMIN:
                nuevo_usuario.is_staff = True
                nuevo_usuario.save(update_fields=['is_staff'])

            Bitacora.objects.create(
                usuario=request.user,
                accion='CREAR_USER',
                entidad='Usuario',
                objeto_id=str(nuevo_usuario.pk),
            )
            messages.success(request, f'Usuario "{username}" creado correctamente.')
            return redirect('administrador:inicio')

        elif accion == 'asignar_doctor':
            paciente_id = request.POST.get('paciente_id', '').strip()
            doctor_id = request.POST.get('doctor_id', '').strip()

            if not paciente_id or not doctor_id:
                messages.error(request, 'Selecciona tanto el paciente como el doctor.')
                return redirect('administrador:inicio')

            paciente = get_object_or_404(PerfilPaciente, id=paciente_id)
            doctor = get_object_or_404(PerfilDoctor, id=doctor_id)

            DoctorPaciente.objects.filter(paciente=paciente, activo=True).exclude(doctor=doctor).update(activo=False)
            asignacion, creada = DoctorPaciente.objects.get_or_create(
                doctor=doctor,
                paciente=paciente,
                defaults={'fecha_inicio': timezone.localdate(), 'activo': True},
            )
            if not creada and not asignacion.activo:
                asignacion.activo = True
                asignacion.fecha_inicio = timezone.localdate()
                asignacion.save(update_fields=['activo', 'fecha_inicio'])

            Bitacora.objects.create(
                usuario=request.user,
                accion='ASIGNAR_DOC',
                entidad='DoctorPaciente',
                objeto_id=str(asignacion.pk),
            )
            messages.success(request, f'Doctor asignado correctamente a {paciente.usuario.get_full_name() or paciente.usuario.username}.')
            return redirect('administrador:inicio')

        elif accion == 'editar_usuario':
            user_id = request.POST.get('user_id', '').strip()
            usuario_obj = get_object_or_404(User, id=user_id)

            nuevo_rol = request.POST.get('rol', usuario_obj.rol).strip().upper()
            usuario_obj.first_name = request.POST.get('first_name', '').strip()
            usuario_obj.last_name = request.POST.get('last_name', '').strip()
            usuario_obj.apellido_materno = request.POST.get('apellido_materno', '').strip()
            usuario_obj.email = request.POST.get('email', '').strip()
            usuario_obj.telefono = request.POST.get('telefono', '').strip()
            if not usuario_obj.is_superuser and nuevo_rol in {
                User.Rol.ADMIN,
                User.Rol.DOCTOR,
                User.Rol.PACIENTE,
            }:
                usuario_obj.rol = nuevo_rol
                usuario_obj.is_staff = nuevo_rol == User.Rol.ADMIN

            usuario_obj.save()

            if usuario_obj.rol == User.Rol.DOCTOR:
                PerfilDoctor.objects.get_or_create(usuario=usuario_obj)
            elif usuario_obj.rol == User.Rol.PACIENTE:
                PerfilPaciente.objects.get_or_create(usuario=usuario_obj)

            Bitacora.objects.create(
                usuario=request.user,
                accion='EDIT_USER',
                entidad='Usuario',
                objeto_id=str(usuario_obj.pk),
            )
            messages.success(request, f'Datos de "{usuario_obj.username}" actualizados.')
            return redirect('administrador:inicio')

        elif accion == 'toggle_usuario':
            user_id = request.POST.get('user_id', '').strip()
            usuario_obj = get_object_or_404(User, id=user_id)

            if usuario_obj == request.user:
                messages.error(request, 'No puedes desactivar tu propia cuenta en sesión.')
                return redirect('administrador:inicio')

            usuario_obj.is_active = not usuario_obj.is_active
            usuario_obj.save(update_fields=['is_active'])

            Bitacora.objects.create(
                usuario=request.user,
                accion='ESTADO_USER',
                entidad='Usuario',
                objeto_id=str(usuario_obj.pk),
            )
            estado_txt = 'activado' if usuario_obj.is_active else 'desactivado'
            messages.success(request, f'Usuario "{usuario_obj.username}" {estado_txt}.')
            return redirect('administrador:inicio')

        elif accion == 'eliminar_usuario':
            user_id = request.POST.get('user_id', '').strip()
            usuario_obj = get_object_or_404(User, id=user_id)

            if usuario_obj == request.user:
                messages.error(request, 'No puedes eliminar tu propia cuenta en sesión.')
                return redirect('administrador:inicio')

            username_eliminado = usuario_obj.username
            id_eliminado = str(usuario_obj.pk)

            try:
                usuario_obj.delete()
            except ProtectedError:
                messages.error(
                    request,
                    f'No se puede eliminar a "{username_eliminado}" porque tiene registros protegidos (como consentimientos o historial clínico). Usa "Desactivar" para darlo de baja sin perder la trazabilidad.',
                )
                return redirect('administrador:inicio')

            Bitacora.objects.create(
                usuario=request.user,
                accion='DEL_USER',
                entidad='Usuario',
                objeto_id=id_eliminado,
            )
            messages.success(request, f'Usuario "{username_eliminado}" eliminado.')
            return redirect('administrador:inicio')

    hoy = timezone.localdate()
    usuarios = User.objects.all().order_by('id')
    doctores = PerfilDoctor.objects.select_related('usuario').all()
    pacientes = PerfilPaciente.objects.select_related('usuario').all()
    asignaciones = DoctorPaciente.objects.select_related('doctor__usuario', 'paciente__usuario').filter(activo=True)
    recetas_qs = Receta.objects.select_related('paciente__usuario', 'doctor__usuario').order_by('-fecha_emision')
    bitacora = Bitacora.objects.select_related('usuario').all()[:50]

    contexto = {
        'total_usuarios': usuarios.count(),
        'total_doctores': doctores.count(),
        'total_pacientes': pacientes.count(),
        'accesos_hoy': Bitacora.objects.filter(fecha__date=hoy).count(),
        'usuarios': usuarios,
        'doctores': doctores,
        'doctores_disponibles': doctores,
        'pacientes': pacientes,
        'asignaciones': asignaciones,
        'recetas': recetas_qs[:20],
        'total_recetas': recetas_qs.count(),
        'bitacora': bitacora,
    }
    return render(request, 'administrador/inicio.html', contexto)