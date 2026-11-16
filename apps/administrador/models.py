from django.conf import settings
from django.db import models


class Bitacora(models.Model):
    """Registro de quién consultó o modificó información. Solo escritura."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bitacora',
    )
    accion = models.CharField(max_length=12)
    entidad = models.CharField(max_length=50)
    objeto_id = models.CharField(max_length=50, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.fecha:%Y-%m-%d %H:%M} {self.usuario} {self.accion} {self.entidad}'