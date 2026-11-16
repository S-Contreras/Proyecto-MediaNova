from django.apps import AppConfig


class AdministradorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.administrador'

    def ready(self):
        from . import signals  # noqa: F401