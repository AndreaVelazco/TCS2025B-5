from rest_framework import serializers
from .models import RegistroFinanciero, ReporteFinanciero, MetaFinanciera

# En finanzas/serializers.py

class RegistroFinancieroSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroFinanciero
        fields = ['id_registro', 'tipo', 'monto', 'fecha', 'categoria', 'descripcion', 'fecha_creacion', 'id_usuario']
        read_only_fields = ['id_registro', 'fecha_creacion', 'id_usuario']  # id_usuario es read_only

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


class DashboardSerializer(serializers.Serializer):
    """Serializer para la respuesta del dashboard financiero.

    Campos:
    - total_ingresos: suma de ingresos del usuario
    - total_gastos: suma de gastos del usuario
    - balance: diferencia ingresos - gastos
    - resumen_por_categoria: lista de {categoria, total} en periodo reciente
    - registros_recientes: últimos registros (lista de dicts)
    - metas_activas: metas activas del usuario (lista de dicts)
    """
    total_ingresos = serializers.FloatField()
    total_gastos = serializers.FloatField()
    balance = serializers.FloatField()
    resumen_por_categoria = serializers.ListField(child=serializers.DictField(), allow_empty=True)
    registros_recientes = serializers.ListField(child=serializers.DictField(), allow_empty=True)
    metas_activas = serializers.ListField(child=serializers.DictField(), allow_empty=True)