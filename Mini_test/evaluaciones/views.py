from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MiniTest, PreguntaTest
from .serializers import (MiniTestSerializer, PreguntaTestSerializer, 
                          RespuestaListSerializer, PreguntaTestAdminSerializer)
from .servicios import ServicioEvaluacion

class MiniTestViewSet(viewsets.ModelViewSet):
    queryset = MiniTest.objects.all()
    serializer_class = MiniTestSerializer
    
    def get_queryset(self):
        return self.queryset.filter(id_usuario=self.request.user)
    
    @action(detail=False, methods=['get'])
    def obtener_preguntas(self, request):
        cantidad = int(request.query_params.get('cantidad', 10))
        preguntas = ServicioEvaluacion.obtener_preguntas_test(cantidad)
        serializer = PreguntaTestSerializer(preguntas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def enviar_respuestas(self, request):
        serializer = RespuestaListSerializer(data=request.data)
        if serializer.is_valid():
            # convertir lista de items a dict esperado por el servicio: {id_pregunta: indice_respuesta}
            respuestas_list = serializer.validated_data['respuestas']
            respuestas_dict = {str(item['pregunta_id']): item['respuesta'] for item in respuestas_list}

            mini_test = ServicioEvaluacion.evaluar_respuestas(
                request.user,
                respuestas_dict
            )
            resultado_serializer = MiniTestSerializer(mini_test)
            return Response(resultado_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def mi_historial(self, request):
        tests = self.get_queryset().order_by('-fecha')[:10]
        serializer = self.get_serializer(tests, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def ultimo_resultado(self, request):
        ultimo_test = self.get_queryset().first()
        if ultimo_test:
            serializer = self.get_serializer(ultimo_test)
            return Response(serializer.data)
        return Response({'mensaje': 'No hay tests realizados'}, status=status.HTTP_404_NOT_FOUND)

class PreguntaTestViewSet(viewsets.ModelViewSet):
    queryset = PreguntaTest.objects.all()
    serializer_class = PreguntaTestAdminSerializer
    
    def get_queryset(self):
        if not self.request.user.is_staff:
            return PreguntaTest.objects.filter(activa=True)
        return self.queryset
