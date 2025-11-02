from .models import MiniTest, PreguntaTest
from aprendizaje.servicios import ServicioRecomendaciones

class ServicioEvaluacion:
    @staticmethod
    def obtener_preguntas_test(cantidad=10):
        """Obtiene preguntas aleatorias para el test"""
        preguntas = PreguntaTest.objects.filter(activa=True).order_by('?')[:cantidad]
        return preguntas
    
    @staticmethod
    def evaluar_respuestas(usuario, respuestas_dict):
        """
        Evalúa las respuestas del usuario y genera el resultado
        respuestas_dict: {id_pregunta: indice_respuesta}
        """
        resultado_por_categoria = {}
        preguntas = PreguntaTest.objects.filter(id_pregunta__in=respuestas_dict.keys())
        
        total_preguntas = len(preguntas)
        respuestas_correctas = 0
        
        for pregunta in preguntas:
            categoria = pregunta.categoria
            if categoria not in resultado_por_categoria:
                resultado_por_categoria[categoria] = {'correctas': 0, 'total': 0}
            
            resultado_por_categoria[categoria]['total'] += 1
            
            respuesta_usuario = respuestas_dict.get(str(pregunta.id_pregunta))
            if respuesta_usuario == pregunta.respuesta_correcta:
                resultado_por_categoria[categoria]['correctas'] += 1
                respuestas_correctas += 1
        
        # Calcular porcentajes por categoría
        resultado_final = {}
        for cat, datos in resultado_por_categoria.items():
            porcentaje = (datos['correctas'] / datos['total'] * 100) if datos['total'] > 0 else 0
            resultado_final[cat] = round(porcentaje, 2)
        
        # Calcular puntuación total
        puntuacion_total = round((respuestas_correctas / total_preguntas * 100), 2) if total_preguntas > 0 else 0
        
        # Determinar nivel
        if puntuacion_total >= 80:
            nivel = 'avanzado'
        elif puntuacion_total >= 50:
            nivel = 'intermedio'
        else:
            nivel = 'principiante'
        
        # Crear registro del test
        mini_test = MiniTest.objects.create(
            id_usuario=usuario,
            resultado=resultado_final,
            puntuacion_total=puntuacion_total,
            nivel_determinado=nivel
        )
        
        # Actualizar perfil del usuario si es diferente
        if usuario.perfil != nivel:
            usuario.perfil = nivel
            usuario.save()
        
        # Generar recomendaciones basadas en el test
        ServicioRecomendaciones.generar_recomendaciones_por_test(usuario, resultado_final)
        
        return mini_test
