from django.db import models

class RecursoAprendizaje(models.Model):
    TIPO_CHOICES = [
        ('video', 'Video'),
        ('articulo', 'Artículo'),
        ('curso', 'Curso'),
        ('podcast', 'Podcast'),
        ('infografia', 'Infografía'),
    ]
    
    TEMATICA_CHOICES = [
        ('presupuesto', 'Presupuesto Personal'),
        ('ahorro', 'Ahorro'),
        ('inversion', 'Inversión'),
        ('deudas', 'Manejo de Deudas'),
        ('credito', 'Crédito'),
        ('impuestos', 'Impuestos'),
        ('emprendimiento', 'Emprendimiento'),
        ('planificacion', 'Planificación Financiera'),
    ]
    
    id_recurso = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    enlace = models.URLField()
    tematica = models.CharField(max_length=30, choices=TEMATICA_CHOICES)
    descripcion = models.TextField()
    nivel = models.CharField(max_length=20, choices=[
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ], default='principiante')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'recurso_aprendizaje'
        verbose_name = 'Recurso de Aprendizaje'
        verbose_name_plural = 'Recursos de Aprendizaje'
    
    def __str__(self):
        return f"{self.titulo} ({self.tipo})"

class Recomendacion(models.Model):
    CRITERIO_CHOICES = [
        ('perfil_usuario', 'Basado en Perfil'),
        ('resultado_test', 'Basado en Test'),
        ('historial_financiero', 'Basado en Historial'),
        ('temas_debiles', 'Basado en Áreas Débiles'),
    ]
    
    id_recomendacion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='recomendaciones')
    id_recurso = models.ForeignKey(RecursoAprendizaje, on_delete=models.CASCADE, related_name='recomendaciones')
    criterio = models.CharField(max_length=30, choices=CRITERIO_CHOICES)
    fecha_recomendacion = models.DateTimeField(auto_now_add=True)
    visto = models.BooleanField(default=False)
    util = models.BooleanField(null=True, blank=True)
    
    class Meta:
        db_table = 'recomendacion'
        verbose_name = 'Recomendación'
        verbose_name_plural = 'Recomendaciones'
    
    def __str__(self):
        return f"Recomendación para {self.id_usuario.nombre}: {self.id_recurso.titulo}"
