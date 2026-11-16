from django.contrib import admin
from .models import PerfilPaciente


@admin.register(PerfilPaciente)
class PerfilPacienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curp', 'fecha_nacimiento', 'sexo', 'tipo_sangre')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'curp')