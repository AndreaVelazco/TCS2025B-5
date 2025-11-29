from django.contrib import admin
from django.utils.html import format_html
from .models import OportunidadEconomica

@admin.register(OportunidadEconomica)
class OportunidadEconomicaAdmin(admin.ModelAdmin):
    list_display = ['nombre_programa', 'tipo', 'institucion', 'monto_formateado', 
                    'fecha_inicio', 'fecha_fin', 'estado_vigencia', 'activa']
    list_filter = ['tipo', 'activa', 'fecha_publicacion']
    search_fields = ['nombre_programa', 'institucion', 'descripcion']
    date_hierarchy = 'fecha_publicacion'
    readonly_fields = ['fecha_publicacion', 'tiempo_restante_display']
    list_per_page = 20
    ordering = ['-fecha_publicacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_programa', 'tipo', 'institucion', 'enlace')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'requisitos', 'monto')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin', 'fecha_publicacion', 'tiempo_restante_display')
        }),
        ('Estado', {
            'fields': ('activa',)
        }),
    )
    
    def monto_formateado(self, obj):
        if obj.monto:
            return f"S/. {obj.monto:,.2f}"
        return "No especificado"
    monto_formateado.short_description = "Monto"
    
    def estado_vigencia(self, obj):
        if obj.esta_vigente:
            color = 'green'
            texto = 'Vigente'
        else:
            color = 'red'
            texto = 'Vencida'
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            texto
        )
    estado_vigencia.short_description = "Estado"
    
    def tiempo_restante_display(self, obj):
        dias = obj.tiempo_restante
        if dias is None:
            return "Sin fecha límite"
        elif dias <= 0:
            return "Vencida"
        return f"{dias} días restantes"
    tiempo_restante_display.short_description = "Tiempo Restante"
    
    actions = ['marcar_como_inactivas', 'marcar_como_activas']
    
    def marcar_como_inactivas(self, request, queryset):
        updated = queryset.update(activa=False)
        self.message_user(request, f'{updated} oportunidades marcadas como inactivas.')
    marcar_como_inactivas.short_description = "Marcar oportunidades seleccionadas como inactivas"
    
    def marcar_como_activas(self, request, queryset):
        updated = queryset.update(activa=True)
        self.message_user(request, f'{updated} oportunidades marcadas como activas.')
    marcar_como_activas.short_description = "Marcar oportunidades seleccionadas como activas"