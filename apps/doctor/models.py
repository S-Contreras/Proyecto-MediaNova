import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class PerfilDoctor(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_doctor',
        limit_choices_to={'rol': 'DOCTOR'},
    )
    cedula_profesional = models.CharField(max_length=20, unique=True)
    especialidad = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Dr(a). {self.usuario.get_full_name() or self.usuario.username}'


class DoctorPaciente(models.Model):
    """Qué doctor atiende (o atendió) a qué paciente."""

    doctor = models.ForeignKey(PerfilDoctor, on_delete=models.PROTECT, related_name='pacientes')
    paciente = models.ForeignKey(
        'paciente.PerfilPaciente', on_delete=models.PROTECT, related_name='doctores'
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)  # se llena si el paciente cambia de médico
    activo = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'paciente', 'fecha_inicio'],
                name='uq_doctor_paciente_inicio',
            )
        ]

    def __str__(self):
        return f'{self.doctor} → {self.paciente}'


def generar_folio():
    return uuid.uuid4().hex[:8].upper()


class Receta(models.Model):
    class Estado(models.TextChoices):
        VIGENTE = 'VIGENTE', 'Vigente'
        SURTIDA = 'SURTIDA', 'Surtida'
        CANCELADA = 'CANCELADA', 'Cancelada'

    folio = models.CharField(max_length=20, unique=True, default=generar_folio, editable=False)
    paciente = models.ForeignKey(
        'paciente.PerfilPaciente', on_delete=models.PROTECT, related_name='recetas'
    )
    doctor = models.ForeignKey(PerfilDoctor, on_delete=models.PROTECT, related_name='recetas')
    fecha_emision = models.DateTimeField(auto_now_add=True)
    diagnostico = models.CharField(max_length=255, blank=True)
    indicaciones = models.TextField(blank=True)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.VIGENTE)

    class Meta:
        ordering = ['-fecha_emision']

    def clean(self):
        # Solo se puede recetar a pacientes que el doctor atiende
        if self.doctor_id and self.paciente_id:
            atiende = DoctorPaciente.objects.filter(
                doctor_id=self.doctor_id, paciente_id=self.paciente_id, activo=True
            ).exists()
            if not atiende:
                raise ValidationError('Este paciente no está asignado activamente a este doctor.')

    def __str__(self):
        return f'Receta {self.folio}'


class DetalleReceta(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='detalles')
    medicamento = models.CharField(max_length=200, help_text='Nombre y concentración')
    dosis = models.CharField(max_length=100)
    frecuencia = models.CharField(max_length=100)
    duracion = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.medicamento} - {self.dosis}'