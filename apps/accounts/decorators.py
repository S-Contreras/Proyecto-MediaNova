from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def rol_requerido(*roles):
    def decorador(vista):
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            if request.user.rol not in roles:
                raise PermissionDenied
            return vista(request, *args, **kwargs)
        return login_required(envoltura)
    return decorador