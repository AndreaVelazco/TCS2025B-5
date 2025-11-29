from .models import RecursoAprendizaje, Recomendacion

class ServicioRecomendaciones:
    @staticmethod
    def generar_recomendaciones_por_test(usuario, resultado_test):
        """Genera recomendaciones basadas en el resultado del test"""
        tematicas_debiles = []
        
        # Mapeo de áreas débiles según puntuación
        if resultado_test.get('presupuesto', 0) < 60:
            tematicas_debiles.append('presupuesto')
        if resultado_test.get('ahorro', 0) < 60:
            tematicas_debiles.append('ahorro')
        if resultado_test.get('inversion', 0) < 60:
            tematicas_debiles.append('inversion')
        if resultado_test.get('deudas', 0) < 60:
            tematicas_debiles.append('deudas')
        
        # Buscar recursos apropiados
        recursos = RecursoAprendizaje.objects.filter(
            tematica__in=tematicas_debiles,
            nivel=usuario.perfil
        )[:5]
        
        # Crear recomendaciones
        recomendaciones = []
        for recurso in recursos:
            rec, created = Recomendacion.objects.get_or_create(
                id_usuario=usuario,
                id_recurso=recurso,
                defaults={
                    'criterio': 'resultado_test'
                }
            )
            if created:
                recomendaciones.append(rec)
        
        return recomendaciones
    
    @staticmethod
    def generar_recomendaciones_por_perfil(usuario):
        """Genera recomendaciones basadas en el perfil del usuario"""
        recursos = RecursoAprendizaje.objects.filter(
            nivel=usuario.perfil
        ).order_by('?')[:3]
        
        recomendaciones = []
        for recurso in recursos:
            rec, created = Recomendacion.objects.get_or_create(
                id_usuario=usuario,
                id_recurso=recurso,
                defaults={
                    'criterio': 'perfil_usuario'
                }
            )
            if created:
                recomendaciones.append(rec)
        
        return recomendaciones