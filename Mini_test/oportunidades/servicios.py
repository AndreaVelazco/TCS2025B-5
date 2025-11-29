from datetime import date
from django.db.models import Q
from .models import OportunidadEconomica

class ServicioOportunidades:
    @staticmethod
    def obtener_oportunidades_vigentes():
        """Obtiene todas las oportunidades vigentes"""
        return OportunidadEconomica.objects.filter(
            Q(fecha_fin__gte=date.today()) | Q(fecha_fin__isnull=True),
            activa=True
        )
    
    @staticmethod
    def obtener_por_tipo_y_monto(tipo=None, monto_min=None, monto_max=None):
        """Obtiene oportunidades filtradas por tipo y rango de monto"""
        queryset = OportunidadEconomica.objects.filter(activa=True)
        
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if monto_min is not None:
            queryset = queryset.filter(monto__gte=monto_min)
        if monto_max is not None:
            queryset = queryset.filter(monto__lte=monto_max)
            
        return queryset
    
    @staticmethod
    def buscar_oportunidades(termino_busqueda):
        """Busca oportunidades por varios campos"""
        return OportunidadEconomica.objects.filter(
            Q(nombre_programa__icontains=termino_busqueda) |
            Q(institucion__icontains=termino_busqueda) |
            Q(descripcion__icontains=termino_busqueda) |
            Q(requisitos__icontains=termino_busqueda),
            activa=True
        )
    
    @staticmethod
    def proximas_a_vencer(dias=30):
        """Obtiene oportunidades próximas a vencer"""
        from datetime import timedelta
        fecha_limite = date.today() + timedelta(days=dias)
        return OportunidadEconomica.objects.filter(
            fecha_fin__lte=fecha_limite,
            fecha_fin__gte=date.today(),
            activa=True
        )