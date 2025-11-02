from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nombre', 'correo', 'perfil', 'fecha_registro']
        read_only_fields = ['id_usuario', 'fecha_registro']

class UsuarioCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'password', 'perfil']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario.objects.create_user(**validated_data, password=password)
        return usuario
