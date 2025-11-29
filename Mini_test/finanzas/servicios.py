from django.db.models import Sum
from datetime import datetime, timedelta, date
from .models import RegistroFinanciero, ReporteFinanciero

class ServicioFinanzas:
    
    @staticmethod
    def obtener_fecha_semana(fecha=None):
        """Obtiene el número de semana y las fechas de inicio/fin de la semana"""
        if fecha is None:
            fecha = date.today()
        
        # Obtener número de semana (ISO: lunes es el primer día)
        semana = fecha.isocalendar()[1]
        anio = fecha.isocalendar()[0]
        
        # Calcular lunes de esa semana
        dia_semana = fecha.weekday()  # 0 = lunes, 6 = domingo
        fecha_inicio = fecha - timedelta(days=dia_semana)
        fecha_fin = fecha_inicio + timedelta(days=6)
        
        return semana, anio, fecha_inicio, fecha_fin
    
    @staticmethod
    def generar_reporte_semanal(usuario, semana=None, anio=None):
        """Genera un reporte financiero para una semana específica"""
        if semana is None or anio is None:
            semana, anio, fecha_inicio, fecha_fin = ServicioFinanzas.obtener_fecha_semana()
        else:
            # Calcular fechas de inicio y fin basado en semana/año
            # Primer día del año
            primer_dia = date(anio, 1, 1)
            # Encontrar el primer lunes del año
            dias_hasta_lunes = (7 - primer_dia.weekday()) % 7
            if dias_hasta_lunes == 0 and primer_dia.weekday() != 0:
                dias_hasta_lunes = 7
            primer_lunes = primer_dia + timedelta(days=dias_hasta_lunes)
            # Calcular fecha de inicio de la semana solicitada
            fecha_inicio = primer_lunes + timedelta(weeks=semana - 1)
            fecha_fin = fecha_inicio + timedelta(days=6)
        
        # Obtener registros de la semana
        registros = RegistroFinanciero.objects.filter(
            id_usuario=usuario,
            fecha__date__gte=fecha_inicio,
            fecha__date__lte=fecha_fin
        )
        
        # Calcular totales
        ingresos = registros.filter(tipo='ingreso')
        gastos = registros.filter(tipo='gasto')
        
        total_ingresos = ingresos.aggregate(total=Sum('monto'))['total'] or 0
        total_gastos = gastos.aggregate(total=Sum('monto'))['total'] or 0
        balance = total_ingresos - total_gastos
        
        # Detalle por categoría
        detalle = {}
        for registro in registros:
            cat = registro.categoria
            if cat not in detalle:
                detalle[cat] = {'ingresos': 0, 'gastos': 0}
            
            if registro.tipo == 'ingreso':
                detalle[cat]['ingresos'] += float(registro.monto)
            else:
                detalle[cat]['gastos'] += float(registro.monto)
        
        # Crear o actualizar reporte
        reporte, created = ReporteFinanciero.objects.update_or_create(
            id_usuario=usuario,
            semana=semana,
            anio=anio,
            defaults={
                'total_ingresos': total_ingresos,
                'total_gastos': total_gastos,
                'balance': balance,
                'detalle_por_categoria': detalle,
                'fecha_inicio_semana': fecha_inicio,
                'fecha_fin_semana': fecha_fin
            }
        )
        
        return reporte
    
    @staticmethod
    def obtener_resumen_anual(usuario, anio):
        """Obtiene resumen de todas las semanas del año"""
        reportes = ReporteFinanciero.objects.filter(
            id_usuario=usuario,
            anio=anio
        ).order_by('semana')
        
        total_ingresos_anual = reportes.aggregate(Sum('total_ingresos'))['total_ingresos__sum'] or 0
        total_gastos_anual = reportes.aggregate(Sum('total_gastos'))['total_gastos__sum'] or 0
        balance_anual = total_ingresos_anual - total_gastos_anual
        
        resumen = {
            'anio': anio,
            'total_semanas': reportes.count(),
            'total_ingresos': float(total_ingresos_anual),
            'total_gastos': float(total_gastos_anual),
            'balance_total': float(balance_anual),
            'reportes_semanales': [
                {
                    'semana': r.semana,
                    'fecha_inicio': r.fecha_inicio_semana.isoformat() if hasattr(r, 'fecha_inicio_semana') else None,
                    'fecha_fin': r.fecha_fin_semana.isoformat() if hasattr(r, 'fecha_fin_semana') else None,
                    'ingresos': float(r.total_ingresos),
                    'gastos': float(r.total_gastos),
                    'balance': float(r.balance)
                }
                for r in reportes
            ]
        }
        
        return resumen
    
    # Mantener compatibilidad con código antiguo (opcional)
    @staticmethod
    def generar_reporte_mensual(usuario, mes, anio):
        """Método legacy - redirige a reporte semanal de la primera semana del mes"""
        primer_dia_mes = date(anio, mes, 1)
        semana, anio_iso, _, _ = ServicioFinanzas.obtener_fecha_semana(primer_dia_mes)
        return ServicioFinanzas.generar_reporte_semanal(usuario, semana, anio_iso)