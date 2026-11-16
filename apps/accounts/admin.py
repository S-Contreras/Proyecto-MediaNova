from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Consentimiento, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Datos del sistema', {'fields': ('rol', 'apellido_materno', 'telefono')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos del sistema', {
            'fields': ('rol', 'first_name', 'last_name', 'apellido_materno', 'telefono'),
        }),
    )
    list_display = ('username', 'first_name', 'last_name', 'rol', 'is_active')
    list_filter = ('rol', 'is_active')

@admin.register(Consentimiento)
class ConsentimientoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'version_aviso', 'datos_salud', 'asistente_expediente', 'estadisticas', 'fecha')
    readonly_fields = [f.name for f in Consentimiento._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False