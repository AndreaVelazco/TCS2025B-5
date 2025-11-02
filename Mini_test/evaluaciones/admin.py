from django.contrib import admin
from .models import MiniTest, PreguntaTest

@admin.register(MiniTest)
class MiniTestAdmin(admin.ModelAdmin):
    list_display = ['id_usuario', 'puntuacion_total', 'nivel_determinado', 'fecha']
    list_filter = ['nivel_determinado', 'fecha']
    search_fields = ['id_usuario__nombre']
    readonly_fields = ['fecha']

@admin.register(PreguntaTest)
class PreguntaTestAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'categoria', 'nivel_dificultad', 'activa']
    list_filter = ['categoria', 'nivel_dificultad', 'activa']
    search_fields = ['pregunta']