from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from .models import RegistroFinanciero, ReporteFinanciero, MetaFinanciera
from .serializers import (RegistroFinancieroSerializer, ReporteFinancieroSerializer, 
                          MetaFinancieraSerializer, DashboardSerializer)
from .servicios import ServicioFinanzas
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

class RegistroFinancieroViewSet(viewsets.ModelViewSet):
    queryset = RegistroFinanciero.objects.all()
    serializer_class = RegistroFinancieroSerializer
    
    def get_queryset(self):
        return self.queryset.filter(id_usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(id_usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def por_mes(self, request):
        mes = int(request.query_params.get('mes', datetime.now().month))
        anio = int(request.query_params.get('anio', datetime.now().year))
        
        registros = self.get_queryset().filter(
            fecha__month=mes,
            fecha__year=anio
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
        mes = int(request.data.get('mes', datetime.now().month))
        anio = int(request.data.get('anio', datetime.now().year))
        
        reporte = ServicioFinanzas.generar_reporte_mensual(request.user, mes, anio)
        serializer = self.get_serializer(reporte)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def reporte_mes(self, request):
        mes = int(request.query_params.get('mes', datetime.now().month))
        anio = int(request.query_params.get('anio', datetime.now().year))
        
        try:
            reporte = ReporteFinanciero.objects.get(
                id_usuario=request.user,
                mes=mes,
                anio=anio
            )
            serializer = self.get_serializer(reporte)
            return Response(serializer.data)
        except ReporteFinanciero.DoesNotExist:
            # Generar el reporte si no existe
            reporte = ServicioFinanzas.generar_reporte_mensual(request.user, mes, anio)
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
    
    POST /api/finanzas/dashboard/ -> agregar ingreso/gasto rápido del mes
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        registros = RegistroFinanciero.objects.filter(id_usuario=user)

        total_ingresos = registros.filter(tipo='ingreso').aggregate(total=Sum('monto'))['total'] or 0
        total_gastos = registros.filter(tipo='gasto').aggregate(total=Sum('monto'))['total'] or 0
        # balance como float
        balance = float(total_ingresos or 0) - float(total_gastos or 0)

        # resumen por categoria en último mes (30 días)
        from datetime import date, timedelta
        fecha_limite = date.today() - timedelta(days=30)
        resumen_query = registros.filter(fecha__gte=fecha_limite).values('categoria').annotate(total=Sum('monto')).order_by('-total')
        resumen_por_categoria = [{'categoria': r['categoria'], 'total': float(r['total'] or 0)} for r in resumen_query]

        # últimos registros
        recientes = registros.order_by('-fecha')[:10]
        registros_recientes = RegistroFinancieroSerializer(recientes, many=True).data

        # metas activas
        metas_activas_qs = MetaFinanciera.objects.filter(id_usuario=user, estado='activa')[:5]
        metas_activas = MetaFinancieraSerializer(metas_activas_qs, many=True).data

        data = {
            'total_ingresos': float(total_ingresos or 0),
            'total_gastos': float(total_gastos or 0),
            'balance': float(balance),
            'resumen_por_categoria': resumen_por_categoria,
            'registros_recientes': registros_recientes,
            'metas_activas': metas_activas,
        }

        return Response(data)
    
    def create(self, request):
        """Agregar un ingreso o gasto rápidamente al mes actual.
        
        Payload:
        {
            "tipo": "ingreso" | "gasto",
            "monto": float,
            "categoria": string,
            "descripcion": string (opcional)
        }
        
        Returns: El registro creado + dashboard actualizado
        """
        tipo = request.data.get('tipo')
        monto = request.data.get('monto')
        categoria = request.data.get('categoria')
        descripcion = request.data.get('descripcion', '')
        
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
        
        # Crear el registro con la fecha de hoy
        from datetime import date
        try:
            registro = RegistroFinanciero.objects.create(
                id_usuario=request.user,
                tipo=tipo,
                monto=float(monto),
                fecha=date.today(),
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