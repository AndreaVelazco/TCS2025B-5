from django.db.models import Sum, Q
from datetime import datetime
from .models import RegistroFinanciero, ReporteFinanciero

class ServicioFinanzas:
    @staticmethod
    def generar_reporte_mensual(usuario, mes, anio):
        """Genera o actualiza el reporte financiero de un mes específico"""
        registros = RegistroFinanciero.objects.filter(
            id_usuario=usuario,
            fecha__month=mes,
            fecha__year=anio
        )
        
        # Calcular totales
        total_ingresos = registros.filter(tipo='ingreso').aggregate(
            total=Sum('monto'))['total'] or 0
        
        total_gastos = registros.filter(tipo='gasto').aggregate(
            total=Sum('monto'))['total'] or 0
        
        balance = total_ingresos - total_gastos
        
        # Detalle por categoría
        detalle = {}
        for registro in registros:
            cat = registro.categoria
            if cat not in detalle:
                detalle[cat] = {'tipo': registro.tipo, 'total': 0}
            detalle[cat]['total'] += float(registro.monto)
        
        # Crear o actualizar reporte
        reporte, created = ReporteFinanciero.objects.update_or_create(
            id_usuario=usuario,
            mes=mes,
            anio=anio,
            defaults={
                'total_ingresos': total_ingresos,
                'total_gastos': total_gastos,
                'balance': balance,
                'detalle_por_categoria': detalle
            }
        )
        
        return reporte
    
    @staticmethod
    def obtener_resumen_anual(usuario, anio):
        """Obtiene el resumen financiero de todo el año"""
        reportes = ReporteFinanciero.objects.filter(
            id_usuario=usuario,
            anio=anio
        )
        
        total_ingresos_anual = reportes.aggregate(Sum('total_ingresos'))['total_ingresos__sum'] or 0
        total_gastos_anual = reportes.aggregate(Sum('total_gastos'))['total_gastos__sum'] or 0
        balance_anual = total_ingresos_anual - total_gastos_anual
        
        return {
            'anio': anio,
            'total_ingresos': total_ingresos_anual,
            'total_gastos': total_gastos_anual,
            'balance': balance_anual,
            'reportes_mensuales': reportes.count()
        }
