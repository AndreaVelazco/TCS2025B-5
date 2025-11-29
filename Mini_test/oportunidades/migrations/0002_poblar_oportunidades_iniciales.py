from django.db import migrations
from datetime import date

def crear_oportunidades_iniciales(apps, schema_editor):
    """Crea las oportunidades económicas iniciales"""
    OportunidadEconomica = apps.get_model('oportunidades', 'OportunidadEconomica')
    
    # Lista de oportunidades iniciales
    oportunidades = [
        {
            'nombre_programa': 'Beca 18',
            'tipo': 'beca',
            'institucion': 'PRONABEC - Perú',
            'enlace': 'https://www.gob.pe/institucion/pronabec/campanias/2093-beca-18',
            'descripcion': 'Programa de becas integrales para estudios superiores dirigido a jóvenes de bajos recursos económicos con alto rendimiento académico.',
            'requisitos': 'Egresado de secundaria, condición de pobreza o pobreza extrema, buen rendimiento académico.',
            'monto': 15000.00,
            'fecha_inicio': date(2025, 1, 15),
            'fecha_fin': date(2025, 12, 31),
            'activa': True,
        },
        {
            'nombre_programa': 'Beca Presidente de la República',
            'tipo': 'beca',
            'institucion': 'PRONABEC - Perú',
            'enlace': 'https://www.gob.pe/institucion/pronabec/campanias/299-beca-presidente-de-la-republica',
            'descripcion': 'Beca para estudios de pregrado en universidades e institutos de excelencia.',
            'requisitos': 'Promedio mínimo de 14, egresado de secundaria, situación de vulnerabilidad económica.',
            'monto': 18000.00,
            'fecha_inicio': date(2025, 2, 1),
            'fecha_fin': date(2025, 11, 30),
            'activa': True,
        },
        {
            'nombre_programa': 'Reactiva Perú - Créditos para MYPEs',
            'tipo': 'credito',
            'institucion': 'Gobierno del Perú',
            'enlace': 'https://www.gob.pe/institucion/mef/campanias/1882-reactiva-peru',
            'descripcion': 'Programa de garantías del gobierno para facilitar créditos a empresas afectadas por la pandemia.',
            'requisitos': 'Ser MYPE formal, no tener deudas en INFOCORP, demostrar afectación económica.',
            'monto': 50000.00,
            'fecha_inicio': date(2025, 1, 1),
            'fecha_fin': date(2025, 6, 30),
            'activa': True,
        },
        {
            'nombre_programa': 'Impulsa Perú - Capacitación Laboral',
            'tipo': 'capacitacion',
            'institucion': 'Ministerio de Trabajo',
            'enlace': 'https://www.gob.pe/institucion/mtpe/campanias/3764-impulsa-peru',
            'descripcion': 'Programa de capacitación gratuita para mejorar la empleabilidad de jóvenes y adultos.',
            'requisitos': 'Mayor de 18 años, DNI vigente, disponibilidad de tiempo.',
            'monto': None,
            'fecha_inicio': date(2025, 3, 1),
            'fecha_fin': date(2025, 12, 15),
            'activa': True,
        },
        {
            'nombre_programa': 'Innovate Perú - Startups',
            'tipo': 'emprendimiento',
            'institucion': 'CONCYTEC',
            'enlace': 'https://www.gob.pe/institucion/concytec/campanias/325-innovate-peru',
            'descripcion': 'Financiamiento no reembolsable para startups de base tecnológica e innovadoras.',
            'requisitos': 'Startup constituida, propuesta innovadora, equipo multidisciplinario.',
            'monto': 80000.00,
            'fecha_inicio': date(2025, 4, 1),
            'fecha_fin': date(2025, 10, 31),
            'activa': True,
        },
        {
            'nombre_programa': 'Tu Empresa - Emprendimientos',
            'tipo': 'emprendimiento',
            'institucion': 'Ministerio de la Producción',
            'enlace': 'https://www.gob.pe/institucion/produce/campanias/338-tu-empresa',
            'descripcion': 'Programa de apoyo integral para emprendedores con asesoría técnica y financiamiento.',
            'requisitos': 'Idea de negocio viable, mayor de 18 años, residir en Perú.',
            'monto': 25000.00,
            'fecha_inicio': date(2025, 2, 15),
            'fecha_fin': date(2025, 11, 30),
            'activa': True,
        },
        {
            'nombre_programa': 'Jóvenes Productivos',
            'tipo': 'empleo',
            'institucion': 'Ministerio de Trabajo',
            'enlace': 'https://www.gob.pe/institucion/mtpe/campanias/318-jovenes-productivos',
            'descripcion': 'Programa de inserción laboral juvenil con capacitación y colocación en empresas.',
            'requisitos': 'Entre 18 y 29 años, secundaria completa, sin experiencia laboral formal.',
            'monto': None,
            'fecha_inicio': date(2025, 1, 10),
            'fecha_fin': date(2025, 12, 20),
            'activa': True,
        },
        {
            'nombre_programa': 'FAE-MYPE - Financiamiento',
            'tipo': 'credito',
            'institucion': 'COFIDE',
            'enlace': 'https://www.gob.pe/9096-acceder-al-fondo-de-apoyo-empresarial-a-la-mype-fae-mype',
            'descripcion': 'Fondo de apoyo empresarial a las micro y pequeñas empresas con tasas preferenciales.',
            'requisitos': 'MYPE formal con RUC activo, no estar en central de riesgo, garantías.',
            'monto': 100000.00,
            'fecha_inicio': date(2025, 1, 5),
            'fecha_fin': date(2025, 12, 31),
            'activa': True,
        },
    ]
    
    # Crear cada oportunidad
    for oportunidad_data in oportunidades:
        # Verificar si ya existe para evitar duplicados
        existe = OportunidadEconomica.objects.filter(
            nombre_programa=oportunidad_data['nombre_programa']
        ).exists()
        
        if not existe:
            OportunidadEconomica.objects.create(**oportunidad_data)


def eliminar_oportunidades_iniciales(apps, schema_editor):
    """Elimina las oportunidades iniciales (para rollback)"""
    OportunidadEconomica = apps.get_model('oportunidades', 'OportunidadEconomica')
    
    nombres_programas = [
        'Beca 18',
        'Beca Presidente de la República',
        'Reactiva Perú - Créditos para MYPEs',
        'Impulsa Perú - Capacitación Laboral',
        'Innovate Perú - Startups',
        'Tu Empresa - Emprendimientos',
        'Jóvenes Productivos',
        'FAE-MYPE - Financiamiento',
    ]
    
    OportunidadEconomica.objects.filter(
        nombre_programa__in=nombres_programas
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('oportunidades', '0001_initial'),  
    ]

    operations = [
        migrations.RunPython(
            crear_oportunidades_iniciales,
            eliminar_oportunidades_iniciales
        ),
    ]