from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import Bitacora


@receiver(user_logged_in)
def registrar_login(sender, request, user, **kwargs):
    Bitacora.objects.create(usuario=user, accion='LOGIN', entidad='Sesión')


@receiver(user_logged_out)
def registrar_logout(sender, request, user, **kwargs):
    Bitacora.objects.create(
        usuario=user if user and user.pk else None, accion='LOGOUT', entidad='Sesión'
    )