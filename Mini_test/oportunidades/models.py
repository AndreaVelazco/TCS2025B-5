from django.db import models

class OportunidadEconomica(models.Model):
    TIPO_CHOICES = [
        ('beca', 'Beca'),
        ('subvencion', 'Subvención'),
        ('credito', 'Crédito Educativo'),
        ('empleo', 'Oportunidad de Empleo'),
        ('capacitacion', 'Capacitación Gratuita'),
        ('emprendimiento', 'Apoyo a Emprendimiento'),
    ]
    
    id_oportunidad = models.AutoField(primary_key=True)
    nombre_programa = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    institucion = models.CharField(max_length=200)
    enlace = models.URLField()
    descripcion = models.TextField()
    requisitos = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'oportunidad_economica'
        verbose_name = 'Oportunidad Económica'
        verbose_name_plural = 'Oportunidades Económicas'
        ordering = ['-fecha_publicacion']
    
    def __str__(self):
        return f"{self.nombre_programa} - {self.institucion}"
    
    @property
    def esta_vigente(self):
        """Verifica si la oportunidad está vigente"""
        from datetime import date
        if not self.fecha_fin:
            return True
        return self.fecha_fin >= date.today()
    
    @property
    def tiempo_restante(self):
        """Calcula el tiempo restante en días"""
        from datetime import date
        if not self.fecha_fin:
            return None
        if not self.esta_vigente:
            return 0
        return (self.fecha_fin - date.today()).days
    
    def actualizar_estado(self):
        """Actualiza el estado activa basado en la fecha de fin"""
        if not self.esta_vigente and self.activa:
            self.activa = False
            self.save()
    
    def save(self, *args, **kwargs):
        """Sobrescribe el método save para validaciones adicionales"""
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio > self.fecha_fin:
                raise ValueError("La fecha de inicio no puede ser posterior a la fecha de fin")
        super().save(*args, **kwargs)
