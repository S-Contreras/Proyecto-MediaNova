from django.contrib import admin
from .models import DetalleReceta, DoctorPaciente, PerfilDoctor, Receta


@admin.register(PerfilDoctor)
class PerfilDoctorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cedula_profesional', 'especialidad')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'cedula_profesional')


@admin.register(DoctorPaciente)
class DoctorPacienteAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'paciente', 'fecha_inicio', 'fecha_fin', 'activo')
    list_filter = ('activo',)


class DetalleRecetaInline(admin.TabularInline):
    model = DetalleReceta
    extra = 1


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('folio', 'paciente', 'doctor', 'fecha_emision', 'estado')
    list_filter = ('estado',)
    readonly_fields = ('folio', 'fecha_emision')
    inlines = [DetalleRecetaInline]