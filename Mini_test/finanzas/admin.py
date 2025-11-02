from django.contrib import admin
from .models import RegistroFinanciero, ReporteFinanciero, MetaFinanciera

@admin.register(RegistroFinanciero)
class RegistroFinancieroAdmin(admin.ModelAdmin):
    list_display = ['id_usuario', 'tipo', 'monto', 'categoria', 'fecha', 'oportunidad']
    list_filter = ['tipo', 'categoria', 'fecha', 'oportunidad']
    search_fields = ['id_usuario__nombre', 'descripcion', 'oportunidad__nombre_programa']
    date_hierarchy = 'fecha'
    autocomplete_fields = ['oportunidad']

@admin.register(ReporteFinanciero)
class ReporteFinancieroAdmin(admin.ModelAdmin):
    list_display = ['id_usuario', 'mes', 'anio', 'total_ingresos', 'total_gastos', 'balance']
    list_filter = ['anio', 'mes']
    search_fields = ['id_usuario__nombre']

@admin.register(MetaFinanciera)
class MetaFinancieraAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'id_usuario', 'monto_actual', 'monto_objetivo', 'estado']
    list_filter = ['estado', 'fecha_inicio']
    search_fields = ['nombre', 'id_usuario__nombre']
