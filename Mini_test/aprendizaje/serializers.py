from rest_framework import serializers
from .models import RecursoAprendizaje, Recomendacion

class RecursoAprendizajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecursoAprendizaje
        fields = '__all__'

class RecomendacionSerializer(serializers.ModelSerializer):
    recurso = RecursoAprendizajeSerializer(source='id_recurso', read_only=True)
    
    class Meta:
        model = Recomendacion
        fields = ['id_recomendacion', 'id_usuario', 'id_recurso', 'recurso', 
                  'criterio', 'fecha_recomendacion', 'visto', 'util']
        read_only_fields = ['id_recomendacion', 'fecha_recomendacion']
