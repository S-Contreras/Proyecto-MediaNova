from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from apps.administrador.models import Bitacora


@receiver(user_logged_in)
def registrar_login(sender, request, user, **kwargs):
    Bitacora.objects.create(
        usuario=user,
        accion='LOGIN',
        entidad='Sesion',
        objeto_id=str(user.pk),
    )


@receiver(user_logged_out)
def registrar_logout(sender, request, user, **kwargs):
    if user and getattr(user, 'pk', None):
        Bitacora.objects.create(
            usuario=user,
            accion='LOGOUT',
            entidad='Sesion',
            objeto_id=str(user.pk),
        )