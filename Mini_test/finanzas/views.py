from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from .models import RegistroFinanciero, ReporteFinanciero, MetaFinanciera
from .serializers import (RegistroFinancieroSerializer, ReporteFinancieroSerializer, 
                          MetaFinancieraSerializer)
from .servicios import ServicioFinanzas

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