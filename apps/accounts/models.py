from django.contrib.auth.models import AbstractUser
from django.db import models


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
