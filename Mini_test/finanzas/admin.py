from django.contrib import admin
from .models import RegistroFinanciero, ReporteFinanciero, MetaFinanciera

@admin.register(RegistroFinanciero)
class RegistroFinancieroAdmin(admin.ModelAdmin):
    list_display = ['id_registro', 'id_usuario', 'tipo', 'monto', 'categoria', 'fecha']
    list_filter = ['tipo', 'categoria', 'fecha']
    search_fields = ['id_usuario__nombre', 'descripcion']
    date_hierarchy = 'fecha'
    ordering = ['-fecha']

@admin.register(ReporteFinanciero)
class ReporteFinancieroAdmin(admin.ModelAdmin):
    list_display = ['id_reporte', 'id_usuario', 'semana', 'anio', 'total_ingresos', 'total_gastos', 'balance', 'fecha_inicio_semana', 'fecha_fin_semana']
    list_filter = ['anio', 'semana']
    search_fields = ['id_usuario__nombre']
    ordering = ['-anio', '-semana']
    readonly_fields = ['fecha_generacion']

@admin.register(MetaFinanciera)
class MetaFinancieraAdmin(admin.ModelAdmin):
    list_display = ['id_meta', 'id_usuario', 'nombre', 'monto_objetivo', 'monto_actual', 'porcentaje_completado', 'estado', 'fecha_objetivo']
    list_filter = ['estado', 'fecha_objetivo']
    search_fields = ['id_usuario__nombre', 'nombre']
    ordering = ['-fecha_objetivo']