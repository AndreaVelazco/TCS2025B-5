from django.db import models
from django.db.models import Sum
from datetime import datetime
from django.utils import timezone

class RegistroFinanciero(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ]
    
    CATEGORIA_CHOICES = [
        # Ingresos
        ('salario', 'Salario'),
        ('freelance', 'Freelance'),
        ('negocio', 'Negocio Propio'),
        ('inversion', 'Inversión'),
        ('otro_ingreso', 'Otro Ingreso'),
        # Gastos
        ('alimentacion', 'Alimentación'),
        ('transporte', 'Transporte'),
        ('vivienda', 'Vivienda'),
        ('servicios', 'Servicios'),
        ('educacion', 'Educación'),
        ('salud', 'Salud'),
        ('entretenimiento', 'Entretenimiento'),
        ('ropa', 'Ropa'),
        ('deudas', 'Pago de Deudas'),
        ('ahorro', 'Ahorro'),
        ('otro_gasto', 'Otro Gasto'),
    ]
    
    id_registro = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='registros_financieros')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    oportunidad = models.ForeignKey('oportunidades.OportunidadEconomica', 
                                  on_delete=models.SET_NULL,
                                  null=True,
                                  blank=True,
                                  related_name='registros_financieros',
                                  help_text='Oportunidad económica relacionada con este registro')
    
    class Meta:
        db_table = 'registro_financiero'
        verbose_name = 'Registro Financiero'
        verbose_name_plural = 'Registros Financieros'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.tipo.capitalize()}: {self.monto} - {self.categoria}"

class ReporteFinanciero(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='reportes_financieros')
    semana = models.IntegerField()  # Número de semana del año (1-52)
    anio = models.IntegerField()
    total_ingresos = models.DecimalField(max_digits=12, decimal_places=2)
    total_gastos = models.DecimalField(max_digits=12, decimal_places=2)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    detalle_por_categoria = models.JSONField()  
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio_semana = models.DateField(null=True, blank=True)  # Primer día de la semana (lunes)
    fecha_fin_semana = models.DateField(null=True, blank=True)     # Último día de la semana (domingo)
    
    class Meta:
        db_table = 'reporte_financiero'
        verbose_name = 'Reporte Financiero'
        verbose_name_plural = 'Reportes Financieros'
        unique_together = ['id_usuario', 'semana', 'anio']
        ordering = ['-anio', '-semana']
    
    def __str__(self):
        return f"Reporte Semana {self.semana}/{self.anio} - {self.id_usuario.nombre}"
        
class MetaFinanciera(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    id_meta = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='metas_financieras')
    nombre = models.CharField(max_length=200)
    monto_objetivo = models.DecimalField(max_digits=12, decimal_places=2)
    monto_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_inicio = models.DateField()
    fecha_objetivo = models.DateField()
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='activa')
    descripcion = models.TextField(blank=True)
    
    class Meta:
        db_table = 'meta_financiera'
        verbose_name = 'Meta Financiera'
        verbose_name_plural = 'Metas Financieras'
    
    def __str__(self):
        return f"{self.nombre} - {self.monto_actual}/{self.monto_objetivo}"
    
    @property
    def porcentaje_completado(self):
        if self.monto_objetivo > 0:
            return round((self.monto_actual / self.monto_objetivo) * 100, 2)
        return 0