from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def rol_requerido(*roles):
    roles_normalizados = {r.upper() for r in roles}

    def decorador(vista):
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            rol_usuario = (getattr(request.user, 'rol', '') or '').upper()
            if rol_usuario not in roles_normalizados:
                raise PermissionDenied
            return vista(request, *args, **kwargs)
        return login_required(envoltura)
    return decorador