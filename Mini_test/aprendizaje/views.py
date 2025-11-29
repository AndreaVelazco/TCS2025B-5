from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import RecursoAprendizaje, Recomendacion
from .serializers import RecursoAprendizajeSerializer, RecomendacionSerializer
from evaluaciones.models import MiniTest, PreguntaTest

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
        """
        Genera recomendaciones personalizadas basadas en el último resultado del minitest
        """
        usuario = request.user
        
        # Obtener el último resultado del test
        ultimo_test = MiniTest.objects.filter(
            id_usuario=usuario
        ).order_by('-fecha').first()
        
        if not ultimo_test:
            # Si no hay resultados, retornar recursos generales
            recursos_generales = RecursoAprendizaje.objects.filter(
                nivel='principiante'
            )[:5]
            
            # Crear recomendaciones si no existen
            for recurso in recursos_generales:
                Recomendacion.objects.get_or_create(
                    id_usuario=usuario,
                    id_recurso=recurso,
                    defaults={
                        'criterio': 'perfil_usuario'
                    }
                )
            
            recomendaciones = self.get_queryset().order_by('-fecha_recomendacion')[:5]
            serializer = self.get_serializer(recomendaciones, many=True)
            return Response(serializer.data)
        
        # Analizar el resultado del test (JSON con categorías y puntuaciones)
        resultado = ultimo_test.resultado
        nivel = ultimo_test.nivel_determinado
        
        # Identificar áreas débiles (categorías con menor puntuación)
        # El resultado es un dict como: {'presupuesto': 2, 'ahorro': 4, 'inversion': 1}
        areas_debiles = sorted(resultado.items(), key=lambda x: x[1])[:3]  # Las 3 más bajas
        
        # Si el nivel es avanzado y todas las puntuaciones son altas
        puntuaciones = list(resultado.values())
        if nivel == 'avanzado' or (puntuaciones and min(puntuaciones) >= 4):
            # Recomendar recursos de nivel intermedio/avanzado
            recursos_avanzados = RecursoAprendizaje.objects.filter(
                nivel__in=['intermedio', 'avanzado']
            ).order_by('?')[:5]
            
            for recurso in recursos_avanzados:
                Recomendacion.objects.get_or_create(
                    id_usuario=usuario,
                    id_recurso=recurso,
                    defaults={
                        'criterio': 'resultado_test'
                    }
                )
        else:
            # Generar recomendaciones para las áreas más débiles
            recursos_recomendados = []
            for categoria, puntuacion in areas_debiles:
                # Buscar recursos relacionados con esta categoría
                recursos = RecursoAprendizaje.objects.filter(
                    tematica=categoria
                ).order_by('?')[:2]  # 2 recursos por categoría
                
                for recurso in recursos:
                    Recomendacion.objects.get_or_create(
                        id_usuario=usuario,
                        id_recurso=recurso,
                        defaults={
                            'criterio': 'temas_debiles'
                        }
                    )
                    recursos_recomendados.append(recurso)
            
            # Si no hay suficientes recursos específicos, agregar algunos generales
            if len(recursos_recomendados) < 5:
                recursos_adicionales = RecursoAprendizaje.objects.exclude(
                    id_recurso__in=[r.id_recurso for r in recursos_recomendados]
                ).order_by('?')[:5 - len(recursos_recomendados)]
                
                for recurso in recursos_adicionales:
                    Recomendacion.objects.get_or_create(
                        id_usuario=usuario,
                        id_recurso=recurso,
                        defaults={
                            'criterio': 'perfil_usuario'
                        }
                    )
        
        # Retornar las recomendaciones más recientes
        recomendaciones = self.get_queryset().order_by('-fecha_recomendacion')[:10]
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