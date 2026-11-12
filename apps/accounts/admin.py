from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Consentimiento, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Rol en el sistema', {'fields': ('rol',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Rol en el sistema', {'fields': ('rol',)}),)
    list_display = ('username', 'email', 'rol', 'is_active')

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