from rest_framework import serializers
from .models import RegistroFinanciero, ReporteFinanciero, MetaFinanciera

class RegistroFinancieroSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroFinanciero
        fields = ['id_registro', 'id_usuario', 'tipo', 'monto', 'fecha', 
                  'categoria', 'descripcion', 'fecha_creacion', 'oportunidad']
        read_only_fields = ['id_registro', 'fecha_creacion']

class ReporteFinancieroSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteFinanciero
        fields = ['id_reporte', 'id_usuario', 'mes', 'anio', 'total_ingresos', 
                  'total_gastos', 'balance', 'detalle_por_categoria', 'fecha_generacion']
        read_only_fields = ['id_reporte', 'fecha_generacion']

class MetaFinancieraSerializer(serializers.ModelSerializer):
    porcentaje_completado = serializers.ReadOnlyField()
    
    class Meta:
        model = MetaFinanciera
        fields = ['id_meta', 'id_usuario', 'nombre', 'monto_objetivo', 
                  'monto_actual', 'fecha_inicio', 'fecha_objetivo', 
                  'estado', 'descripcion', 'porcentaje_completado']
        read_only_fields = ['id_meta']