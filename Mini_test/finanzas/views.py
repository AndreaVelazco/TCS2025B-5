from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timedelta, date
from .models import RegistroFinanciero, ReporteFinanciero, MetaFinanciera
from .serializers import (RegistroFinancieroSerializer, ReporteFinancieroSerializer, 
                          MetaFinancieraSerializer, DashboardSerializer)
from .servicios import ServicioFinanzas
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum


class RegistroFinancieroViewSet(viewsets.ModelViewSet):
    queryset = RegistroFinanciero.objects.all()
    serializer_class = RegistroFinancieroSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(id_usuario=self.request.user)
    
    def perform_create(self, serializer):
        """Asignar automáticamente el usuario autenticado al crear un registro"""
        from django.utils import timezone
        from django.utils.dateparse import parse_datetime
        
        # Obtener fecha del request
        fecha_str = self.request.data.get('fecha')
        
        if fecha_str:
            # Convertir fecha ISO a datetime con zona horaria
            fecha_dt = parse_datetime(fecha_str)
            if fecha_dt:
                # Asegurar que tenga zona horaria
                if timezone.is_naive(fecha_dt):
                    fecha_dt = timezone.make_aware(fecha_dt)
                # Convertir a hora local de Lima
                fecha = timezone.localtime(fecha_dt)
            else:
                fecha = timezone.localtime(timezone.now())
        else:
            fecha = timezone.localtime(timezone.now())
        
        # Guardar con el usuario autenticado y la fecha procesada
        serializer.save(id_usuario=self.request.user, fecha=fecha)
    
    @action(detail=False, methods=['get'])
    def por_semana(self, request):
        """Obtener registros de la semana actual o específica"""
        semana = request.query_params.get('semana')
        anio = request.query_params.get('anio')
        
        if semana and anio:
            semana = int(semana)
            anio = int(anio)
            # Calcular fechas de la semana
            primer_dia = date(anio, 1, 1)
            dias_hasta_lunes = (7 - primer_dia.weekday()) % 7
            if dias_hasta_lunes == 0 and primer_dia.weekday() != 0:
                dias_hasta_lunes = 7
            primer_lunes = primer_dia + timedelta(days=dias_hasta_lunes)
            fecha_inicio = primer_lunes + timedelta(weeks=semana - 1)
            fecha_fin = fecha_inicio + timedelta(days=6)
        else:
            # Semana actual
            semana, anio, fecha_inicio, fecha_fin = ServicioFinanzas.obtener_fecha_semana()
        
        registros = self.get_queryset().filter(
            fecha__date__gte=fecha_inicio,
            fecha__date__lte=fecha_fin
        )
        serializer = self.get_serializer(registros, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        categoria = request.query_params.get('categoria')
        if not categoria:
            return Response({'error': 'Parámetro categoria requerido'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        registros = self.get_queryset().filter(categoria=categoria)
        serializer = self.get_serializer(registros, many=True)
        return Response(serializer.data)


class ReporteFinancieroViewSet(viewsets.ModelViewSet):
    queryset = ReporteFinanciero.objects.all()
    serializer_class = ReporteFinancieroSerializer
    
    def get_queryset(self):
        return self.queryset.filter(id_usuario=self.request.user)
    
    @action(detail=False, methods=['post'])
    def generar_reporte(self, request):
        """Generar reporte de una semana específica"""
        semana = request.data.get('semana')
        anio = request.data.get('anio')
        
        if semana and anio:
            semana = int(semana)
            anio = int(anio)
        else:
            semana, anio, _, _ = ServicioFinanzas.obtener_fecha_semana()
        
        reporte = ServicioFinanzas.generar_reporte_semanal(request.user, semana, anio)
        serializer = self.get_serializer(reporte)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def reporte_semana(self, request):
        """Obtener reporte de una semana específica"""
        semana = request.query_params.get('semana')
        anio = request.query_params.get('anio')
        
        if semana and anio:
            semana = int(semana)
            anio = int(anio)
        else:
            semana, anio, _, _ = ServicioFinanzas.obtener_fecha_semana()
        
        try:
            reporte = ReporteFinanciero.objects.get(
                id_usuario=request.user,
                semana=semana,
                anio=anio
            )
            serializer = self.get_serializer(reporte)
            return Response(serializer.data)
        except ReporteFinanciero.DoesNotExist:
            # Generar el reporte si no existe
            reporte = ServicioFinanzas.generar_reporte_semanal(request.user, semana, anio)
            serializer = self.get_serializer(reporte)
            return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def resumen_anual(self, request):
        anio = int(request.query_params.get('anio', datetime.now().year))
        resumen = ServicioFinanzas.obtener_resumen_anual(request.user, anio)
        return Response(resumen)


class MetaFinancieraViewSet(viewsets.ModelViewSet):
    queryset = MetaFinanciera.objects.all()
    serializer_class = MetaFinancieraSerializer
    
    def get_queryset(self):
        return self.queryset.filter(id_usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(id_usuario=self.request.user)
    
    @action(detail=True, methods=['post'])
    def agregar_monto(self, request, pk=None):
        meta = self.get_object()
        monto = request.data.get('monto')
        
        if not monto:
            return Response({'error': 'Parámetro monto requerido'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        meta.monto_actual += float(monto)
        if meta.monto_actual >= meta.monto_objetivo:
            meta.estado = 'completada'
        meta.save()
        
        serializer = self.get_serializer(meta)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def activas(self, request):
        metas = self.get_queryset().filter(estado='activa')
        serializer = self.get_serializer(metas, many=True)
        return Response(serializer.data)


class DashboardViewSet(viewsets.ViewSet):
    """Endpoint para el dashboard financiero del usuario.

    GET /api/finanzas/dashboard/ -> devuelve totales, resumen por categoría,
    últimos movimientos y metas activas.
    
    POST /api/finanzas/dashboard/ -> agregar ingreso/gasto rápido de la semana
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        
        # Obtener semana actual
        semana, anio, fecha_inicio, fecha_fin = ServicioFinanzas.obtener_fecha_semana()
        
        # Filtrar registros de la semana actual
        registros = RegistroFinanciero.objects.filter(
            id_usuario=user,
            fecha__date__gte=fecha_inicio,
            fecha__date__lte=fecha_fin
        )

        total_ingresos = registros.filter(tipo='ingreso').aggregate(total=Sum('monto'))['total'] or 0
        total_gastos = registros.filter(tipo='gasto').aggregate(total=Sum('monto'))['total'] or 0
        balance = float(total_ingresos or 0) - float(total_gastos or 0)

        # Resumen por categoría de la semana
        resumen_query = registros.values('categoria').annotate(total=Sum('monto')).order_by('-total')
        resumen_por_categoria = [{'categoria': r['categoria'], 'total': float(r['total'] or 0)} for r in resumen_query]

        # Últimos registros
        recientes = RegistroFinanciero.objects.filter(id_usuario=user).order_by('-fecha')[:10]
        registros_recientes = RegistroFinancieroSerializer(recientes, many=True).data

        # Metas activas
        metas_activas_qs = MetaFinanciera.objects.filter(id_usuario=user, estado='activa')[:5]
        metas_activas = MetaFinancieraSerializer(metas_activas_qs, many=True).data

        data = {
            'semana_actual': semana,
            'anio_actual': anio,
            'fecha_inicio_semana': fecha_inicio.isoformat(),
            'fecha_fin_semana': fecha_fin.isoformat(),
            'total_ingresos': float(total_ingresos or 0),
            'total_gastos': float(total_gastos or 0),
            'balance': float(balance),
            'resumen_por_categoria': resumen_por_categoria,
            'registros_recientes': registros_recientes,
            'metas_activas': metas_activas,
        }

        return Response(data)
    
    def create(self, request):
        """Agregar un ingreso o gasto rápidamente a la semana actual.
        
        Payload:
        {
            "tipo": "ingreso" | "gasto",
            "monto": float,
            "categoria": string,
            "descripcion": string (opcional),
            "fecha": string ISO (opcional)
        }
        
        Returns: El registro creado
        """
        from django.utils import timezone
        from django.utils.dateparse import parse_datetime
        
        tipo = request.data.get('tipo')
        monto = request.data.get('monto')
        categoria = request.data.get('categoria')
        descripcion = request.data.get('descripcion', '')
        fecha_str = request.data.get('fecha')
        
        # Validar campos requeridos
        if not all([tipo, monto, categoria]):
            return Response(
                {'error': 'Se requieren: tipo, monto, categoria'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar tipo
        if tipo not in ['ingreso', 'gasto']:
            return Response(
                {'error': 'tipo debe ser "ingreso" o "gasto"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Procesar fecha
        if fecha_str:
            fecha_dt = parse_datetime(fecha_str)
            if fecha_dt:
                if timezone.is_naive(fecha_dt):
                    fecha_dt = timezone.make_aware(fecha_dt)
                fecha = timezone.localtime(fecha_dt)
            else:
                fecha = timezone.localtime(timezone.now())
        else:
            fecha = timezone.localtime(timezone.now())
        
        # Crear el registro
        try:
            registro = RegistroFinanciero.objects.create(
                id_usuario=request.user,
                tipo=tipo,
                monto=float(monto),
                fecha=fecha,
                categoria=categoria,
                descripcion=descripcion
            )
            
            # Retornar el registro creado
            registro_serializer = RegistroFinancieroSerializer(registro)
            return Response(registro_serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': f'Error al crear registro: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )