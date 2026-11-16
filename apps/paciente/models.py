from django.conf import settings
from django.db import models


class PerfilPaciente(models.Model):
    class Sexo(models.TextChoices):
        FEMENINO = 'F', 'Femenino'
        MASCULINO = 'M', 'Masculino'
        OTRO = 'O', 'Otro'

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_paciente',
        limit_choices_to={'rol': 'PACIENTE'},
    )
    curp = models.CharField(max_length=18, unique=True, null=True, blank=True)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    tipo_sangre = models.CharField(max_length=3, blank=True)
    alergias = models.TextField(blank=True)
    padecimientos = models.TextField(blank=True, help_text='Enfermedades y su seguimiento')

    def __str__(self):
        return f'{self.usuario.get_full_name() or self.usuario.username}'