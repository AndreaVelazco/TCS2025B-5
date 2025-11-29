from rest_framework import serializers
from .models import MiniTest, PreguntaTest
import json


class PreguntaTestSerializer(serializers.ModelSerializer):
    opciones = serializers.SerializerMethodField()
    
    class Meta:
        model = PreguntaTest
        fields = ['id_pregunta', 'categoria', 'pregunta', 'opciones', 'nivel_dificultad']
    
    def get_opciones(self, obj):
        """
        Convierte las opciones de JSON string a lista
        """
        if isinstance(obj.opciones, str):
            try:
                return json.loads(obj.opciones)
            except (json.JSONDecodeError, TypeError):
                return []
        elif isinstance(obj.opciones, list):
            return obj.opciones
        else:
            return []


class PreguntaTestAdminSerializer(serializers.ModelSerializer):
    respuesta_correcta = serializers.IntegerField(required=False, allow_null=True)
    opciones = serializers.SerializerMethodField()
    
    class Meta:
        model = PreguntaTest
        fields = '__all__'
    
    def get_opciones(self, obj):
        """
        Convierte las opciones de JSON string a lista
        """
        if isinstance(obj.opciones, str):
            try:
                return json.loads(obj.opciones)
            except (json.JSONDecodeError, TypeError):
                return []
        elif isinstance(obj.opciones, list):
            return obj.opciones
        else:
            return []

    def _normalize_opciones(self, opciones):
        """
        Acepta opciones en dos formatos:
        - lista de strings: ["opA", "opB"]
        - lista de objetos: [{"texto": "opA", "correcta": False}, {"texto": "opB", "correcta": True}]

        Devuelve (opciones_texto_list, respuesta_correcta_index_or_None)
        """
        if not opciones:
            return [], None

        # si elementos son dicts, extraer texto y buscar el índice marcado como correcta
        if isinstance(opciones, list) and len(opciones) > 0 and isinstance(opciones[0], dict):
            opciones_texto = []
            correcta_index = None
            for idx, opt in enumerate(opciones):
                texto = opt.get('texto') if isinstance(opt, dict) else opt
                opciones_texto.append(texto)
                if isinstance(opt, dict) and opt.get('correcta'):
                    # tomar la primera marcada como correcta
                    if correcta_index is None:
                        correcta_index = idx
            return opciones_texto, correcta_index

        # caso por defecto: lista de strings
        return opciones, None

    def create(self, validated_data):
        opciones = validated_data.get('opciones')
        opciones_texto, correcta_index = self._normalize_opciones(opciones)
        # Si el payload incluye respuesta_correcta explícita, la respetamos
        if 'respuesta_correcta' in validated_data and validated_data.get('respuesta_correcta') is not None:
            respuesta_correcta = validated_data.pop('respuesta_correcta')
        else:
            respuesta_correcta = correcta_index

        # Guardar como JSON string
        validated_data['opciones'] = json.dumps(opciones_texto)
        if respuesta_correcta is not None:
            validated_data['respuesta_correcta'] = respuesta_correcta

        return super().create(validated_data)

    def update(self, instance, validated_data):
        opciones = validated_data.get('opciones')
        if opciones is not None:
            opciones_texto, correcta_index = self._normalize_opciones(opciones)
            # Guardar como JSON string
            validated_data['opciones'] = json.dumps(opciones_texto)
            if 'respuesta_correcta' in validated_data and validated_data.get('respuesta_correcta') is not None:
                # se respetará la respuesta_correcta proveniente del payload
                pass
            elif correcta_index is not None:
                validated_data['respuesta_correcta'] = correcta_index

        return super().update(instance, validated_data)


class MiniTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiniTest
        fields = ['id_test', 'id_usuario', 'resultado', 'puntuacion_total', 
                  'nivel_determinado', 'fecha']
        read_only_fields = ['id_test', 'fecha']


class RespuestaItemSerializer(serializers.Serializer):
    pregunta_id = serializers.IntegerField()
    respuesta = serializers.IntegerField()


class RespuestaListSerializer(serializers.Serializer):
    respuestas = RespuestaItemSerializer(many=True)
    
    def validate_respuestas(self, value):
        # asegurar que no hay ids repetidos
        ids = [item['pregunta_id'] for item in value]
        if len(ids) != len(set(ids)):
            raise serializers.ValidationError('Hay preguntas repetidas en las respuestas')
        return value