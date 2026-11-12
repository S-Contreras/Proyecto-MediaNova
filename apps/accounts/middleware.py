from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class ConsentimientoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        usuario = request.user
        if usuario.is_authenticated and usuario.rol == 'PACIENTE':
            libres = [reverse('consentimiento'), reverse('aviso_privacidad'), reverse('logout')]
            if request.path not in libres and not request.path.startswith(settings.STATIC_URL):
                acepto = usuario.consentimientos.filter(
                    version_aviso=settings.AVISO_VERSION, datos_salud=True
                ).exists()
                if not acepto:
                    return redirect('consentimiento')
        return self.get_response(request)