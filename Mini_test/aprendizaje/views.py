from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RecursoAprendizaje, Recomendacion
from .serializers import RecursoAprendizajeSerializer, RecomendacionSerializer

class RecursoAprendizajeViewSet(viewsets.ModelViewSet):
    queryset = RecursoAprendizaje.objects.all()
    serializer_class = RecursoAprendizajeSerializer
    
    @action(detail=False, methods=['get'])
    def por_tematica(self, request):
        tematica = request.query_params.get('tematica')
        if not tematica:
            return Response({'error': 'Parámetro tematica requerido'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        recursos = self.queryset.filter(tematica=tematica)
        serializer = self.get_serializer(recursos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_nivel(self, request):
        nivel = request.query_params.get('nivel', request.user.perfil)
        recursos = self.queryset.filter(nivel=nivel)
        serializer = self.get_serializer(recursos, many=True)
        return Response(serializer.data)

class RecomendacionViewSet(viewsets.ModelViewSet):
    queryset = Recomendacion.objects.all()
    serializer_class = RecomendacionSerializer
    
    def get_queryset(self):
        return self.queryset.filter(id_usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def mis_recomendaciones(self, request):
        recomendaciones = self.get_queryset().filter(visto=False).order_by('-fecha_recomendacion')
        serializer = self.get_serializer(recomendaciones, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def marcar_visto(self, request, pk=None):
        recomendacion = self.get_object()
        recomendacion.visto = True
        recomendacion.save()
        return Response({'mensaje': 'Marcado como visto'})
    
    @action(detail=True, methods=['post'])
    def calificar(self, request, pk=None):
        recomendacion = self.get_object()
        util = request.data.get('util')
        if util is not None:
            recomendacion.util = util
            recomendacion.save()
            return Response({'mensaje': 'Calificación guardada'})
        return Response({'error': 'Parámetro util requerido'}, 
                       status=status.HTTP_400_BAD_REQUEST)