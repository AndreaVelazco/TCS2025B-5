from django.contrib import admin
from .models import RecursoAprendizaje, Recomendacion

@admin.register(RecursoAprendizaje)
class RecursoAprendizajeAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'tematica', 'nivel', 'fecha_creacion']
    list_filter = ['tipo', 'tematica', 'nivel']
    search_fields = ['titulo', 'descripcion']

@admin.register(Recomendacion)
class RecomendacionAdmin(admin.ModelAdmin):
    list_display = ['id_usuario', 'id_recurso', 'criterio', 'fecha_recomendacion', 'visto', 'util']
    list_filter = ['criterio', 'visto', 'util', 'fecha_recomendacion']
    search_fields = ['id_usuario__nombre', 'id_recurso__titulo']