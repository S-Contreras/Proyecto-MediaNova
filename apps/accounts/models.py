from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    class Rol(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        DOCTOR = 'DOCTOR', 'Doctor'
        PACIENTE = 'PACIENTE', 'Paciente'

    rol = models.CharField(max_length=10, choices=Rol.choices, default=Rol.PACIENTE)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.rol = self.Rol.ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.username} ({self.get_rol_display()})'

class Consentimiento(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='consentimientos')
    version_aviso = models.CharField(max_length=10)
    datos_salud = models.BooleanField()
    asistente_expediente = models.BooleanField(default=False)
    estadisticas = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.usuario} · v{self.version_aviso} · {self.fecha:%Y-%m-%d}'
