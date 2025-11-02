from django.db import models
import json

class MiniTest(models.Model):
    id_test = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='tests')
    resultado = models.JSONField()  # Almacena {categoria: puntuacion}
    puntuacion_total = models.IntegerField()
    nivel_determinado = models.CharField(max_length=20, choices=[
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ])
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'minitest'
        verbose_name = 'Mini Test'
        verbose_name_plural = 'Mini Tests'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"Test de {self.id_usuario.nombre} - {self.fecha.strftime('%d/%m/%Y')}"

class PreguntaTest(models.Model):
    CATEGORIA_CHOICES = [
        ('presupuesto', 'Presupuesto Personal'),
        ('ahorro', 'Ahorro'),
        ('inversion', 'Inversión'),
        ('deudas', 'Manejo de Deudas'),
        ('credito', 'Crédito'),
    ]
    
    id_pregunta = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES)
    pregunta = models.TextField()
    opciones = models.JSONField()  # Lista de opciones
    respuesta_correcta = models.IntegerField()  # Índice de la respuesta correcta
    explicacion = models.TextField(blank=True)
    nivel_dificultad = models.CharField(max_length=20, choices=[
        ('facil', 'Fácil'),
        ('medio', 'Medio'),
        ('dificil', 'Difícil'),
    ], default='medio')
    activa = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'pregunta_test'
        verbose_name = 'Pregunta de Test'
        verbose_name_plural = 'Preguntas de Test'
    
    def __str__(self):
        return f"{self.categoria}: {self.pregunta[:50]}..."