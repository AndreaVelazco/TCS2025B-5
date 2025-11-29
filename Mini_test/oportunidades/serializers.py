from rest_framework import serializers
from .models import OportunidadEconomica

class OportunidadEconomicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OportunidadEconomica
        fields = '__all__'
