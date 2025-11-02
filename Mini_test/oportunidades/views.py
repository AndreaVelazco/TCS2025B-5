from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import OportunidadEconomica
from .serializers import OportunidadEconomicaSerializer
from .servicios import ServicioOportunidades

class OportunidadEconomicaViewSet(viewsets.ModelViewSet):
    queryset = OportunidadEconomica.objects.filter(activa=True)
    serializer_class = OportunidadEconomicaSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'institucion']
    search_fields = ['nombre_programa', 'descripcion', 'institucion']
    ordering_fields = ['fecha_publicacion', 'fecha_inicio', 'fecha_fin', 'monto']
    ordering = ['-fecha_publicacion']
    
    @action(detail=False, methods=['get'])
    def por_tipo(self, request):
        tipo = request.query_params.get('tipo')
        if not tipo:
            return Response({'error': 'Parámetro tipo requerido'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        oportunidades = self.queryset.filter(tipo=tipo)
        serializer = self.get_serializer(oportunidades, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def vigentes(self, request):
        from datetime import date
        oportunidades = self.queryset.filter(
            fecha_fin__gte=date.today()
        ) | self.queryset.filter(fecha_fin__isnull=True)
        serializer = self.get_serializer(oportunidades, many=True)
        return Response(serializer.data)