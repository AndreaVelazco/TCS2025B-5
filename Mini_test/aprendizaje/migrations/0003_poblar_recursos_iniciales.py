from django.db import migrations

def crear_recursos_iniciales(apps, schema_editor):
    """Crea los recursos de aprendizaje iniciales"""
    RecursoAprendizaje = apps.get_model('aprendizaje', 'RecursoAprendizaje')
    
    recursos = [
        # === PRESUPUESTO PERSONAL ===
        {
            'tipo': 'video',
            'titulo': 'Cómo hacer un presupuesto mensual efectivo',
            'enlace': 'https://www.youtube.com/watch?v=ejemplo1',
            'tematica': 'presupuesto',
            'descripcion': 'Aprende a crear un presupuesto personal paso a paso, identificando ingresos, gastos fijos y variables.',
            'nivel': 'principiante',
        },
        {
            'tipo': 'articulo',
            'titulo': 'Método 50/30/20 para distribuir tu sueldo',
            'enlace': 'https://www.bcp.com.pe/educacion-financiera/presupuesto-5030020',
            'tematica': 'presupuesto',
            'descripcion': 'Conoce la regla 50/30/20 para dividir tus ingresos: 50% necesidades, 30% gustos, 20% ahorro.',
            'nivel': 'principiante',
        },
        {
            'tipo': 'curso',
            'titulo': 'Presupuesto familiar avanzado',
            'enlace': 'https://www.coursera.org/learn/presupuesto-familiar',
            'tematica': 'presupuesto',
            'descripcion': 'Curso completo sobre planificación de presupuesto familiar con herramientas digitales.',
            'nivel': 'intermedio',
        },
        
        # === AHORRO ===
        {
            'tipo': 'video',
            'titulo': 'Introducción al ahorro: Primeros pasos',
            'enlace': 'https://www.youtube.com/watch?v=ejemplo2',
            'tematica': 'ahorro',
            'descripcion': 'Descubre por qué es importante ahorrar y cómo empezar con poco dinero.',
            'nivel': 'principiante',
        },
        {
            'tipo': 'articulo',
            'titulo': 'Fondo de emergencia: ¿Cuánto necesitas?',
            'enlace': 'https://www.sbs.gob.pe/educacion-financiera/fondo-emergencia',
            'tematica': 'ahorro',
            'descripcion': 'Aprende a calcular y construir tu fondo de emergencia de 3 a 6 meses de gastos.',
            'nivel': 'intermedio',
        },
        {
            'tipo': 'infografia',
            'titulo': '10 tips para ahorrar dinero todos los días',
            'enlace': 'https://www.bbva.pe/educacion-financiera/infografia-ahorro',
            'tematica': 'ahorro',
            'descripcion': 'Infografía con consejos prácticos para reducir gastos y aumentar el ahorro.',
            'nivel': 'principiante',
        },
        {
            'tipo': 'curso',
            'titulo': 'Estrategias avanzadas de ahorro e inversión',
            'enlace': 'https://www.edx.org/course/ahorro-avanzado',
            'tematica': 'ahorro',
            'descripcion': 'Técnicas sofisticadas de ahorro sistemático y preparación para invertir.',
            'nivel': 'avanzado',
        },
        
        # === INVERSIÓN ===
        {
            'tipo': 'video',
            'titulo': '¿Qué es invertir? Conceptos básicos',
            'enlace': 'https://www.youtube.com/watch?v=ejemplo3',
            'tematica': 'inversion',
            'descripcion': 'Introducción al mundo de las inversiones: acciones, bonos y fondos mutuos.',
            'nivel': 'principiante',
        },
        {
            'tipo': 'articulo',
            'titulo': 'Inversión en la Bolsa de Valores de Lima',
            'enlace': 'https://www.bvl.com.pe/educacion/invierte-en-bolsa',
            'tematica': 'inversion',
            'descripcion': 'Guía para comenzar a invertir en la Bolsa de Valores de Lima (BVL).',
            'nivel': 'intermedio',
        },
        {
            'tipo': 'curso',
            'titulo': 'Fondos mutuos y AFP en Perú',
            'enlace': 'https://www.sbs.gob.pe/cursos/fondos-mutuos',
            'tematica': 'inversion',
            'descripcion': 'Curso sobre cómo funcionan los fondos mutuos y las AFP en el sistema peruano.',
            'nivel': 'intermedio',
        },
        {
            'tipo': 'podcast',
            'titulo': 'Diversificación de cartera de inversiones',
            'enlace': 'https://open.spotify.com/show/inversion-inteligente',
            'tematica': 'inversion',
            'descripcion': 'Episodio sobre cómo diversificar inversiones para reducir riesgos.',
            'nivel': 'avanzado',
        },
        
        # === MANEJO DE DEUDAS ===
        {
            'tipo': 'video',
            'titulo': 'Cómo salir de deudas: Método bola de nieve',
            'enlace': 'https://www.youtube.com/watch?v=ejemplo4',
            'tematica': 'deudas',
            'descripcion': 'Estrategia para pagar deudas de menor a mayor y ganar impulso financiero.',
            'nivel': 'principiante',
        },
        {
            'tipo': 'articulo',
            'titulo': 'Refinanciamiento vs. Consolidación de deudas',
            'enlace': 'https://www.sbs.gob.pe/educacion/deudas-refinanciamiento',
            'tematica': 'deudas',
            'descripcion': 'Conoce las diferencias y cuándo conviene cada opción.',
            'nivel': 'intermedio',
        },
        {
            'tipo': 'infografia',
            'titulo': 'Señales de alerta: Sobreendeudamiento',
            'enlace': 'https://www.sbs.gob.pe/alertas-deuda',
            'tematica': 'deudas',
            'descripcion': 'Identifica cuándo tus deudas están fuera de control.',
            'nivel': 'principiante',
        },
        
        # === CRÉDITO ===
        {
            'tipo': 'video',
            'titulo': 'Historial crediticio: ¿Qué es y por qué importa?',
            'enlace': 'https://www.youtube.com/watch?v=ejemplo5',
            'tematica': 'credito',
            'descripcion': 'Aprende sobre el score crediticio y cómo mejorarlo en centrales de riesgo.',
            'nivel': 'principiante',
        },
        {
            'tipo': 'articulo',
            'titulo': 'Tipos de créditos en el sistema financiero peruano',
            'enlace': 'https://www.sbs.gob.pe/tipos-de-credito',
            'tematica': 'credito',
            'descripcion': 'Créditos de consumo, hipotecarios, vehiculares y microcréditos explicados.',
            'nivel': 'intermedio',
        },
        {
            'tipo': 'curso',
            'titulo': 'Cómo negociar mejores tasas de interés',
            'enlace': 'https://www.asbanc.com.pe/cursos/negociacion-creditos',
            'tematica': 'credito',
            'descripcion': 'Estrategias para conseguir mejores condiciones crediticias.',
            'nivel': 'avanzado',
        },
        
        # === IMPUESTOS ===
        {
            'tipo': 'video',
            'titulo': 'Impuestos básicos en Perú: IGV y Renta',
            'enlace': 'https://www.youtube.com/watch?v=ejemplo6',
            'tematica': 'impuestos',
            'descripcion': 'Introducción al sistema tributario peruano para personas naturales.',
            'nivel': 'principiante',
        },
        {
            'tipo': 'articulo',
            'titulo': 'Declaración anual de Impuesto a la Renta',
            'enlace': 'https://www.sunat.gob.pe/educacion/declaracion-renta',
            'tematica': 'impuestos',
            'descripcion': 'Guía paso a paso para declarar tu renta anual ante SUNAT.',
            'nivel': 'intermedio',
        },
        {
            'tipo': 'curso',
            'titulo': 'Planificación tributaria para profesionales independientes',
            'enlace': 'https://www.sunat.gob.pe/cursos/independientes',
            'tematica': 'impuestos',
            'descripcion': 'Optimiza tu carga tributaria de manera legal si eres freelance.',
            'nivel': 'avanzado',
        },
        
        # === EMPRENDIMIENTO ===
        {
            'tipo': 'video',
            'titulo': 'Cómo empezar un negocio con poco dinero',
            'enlace': 'https://www.youtube.com/watch?v=ejemplo7',
            'tematica': 'emprendimiento',
            'descripcion': 'Ideas y estrategias para emprendedores con capital limitado.',
            'nivel': 'principiante',
        },
        {
            'tipo': 'articulo',
            'titulo': 'Formalización de tu emprendimiento en Perú',
            'enlace': 'https://www.gob.pe/empresa/formalizacion',
            'tematica': 'emprendimiento',
            'descripcion': 'Pasos para constituir tu empresa y obtener RUC.',
            'nivel': 'intermedio',
        },
        {
            'tipo': 'podcast',
            'titulo': 'Casos de éxito: Emprendedores peruanos',
            'enlace': 'https://open.spotify.com/show/emprendedores-peru',
            'tematica': 'emprendimiento',
            'descripcion': 'Entrevistas con empresarios exitosos del Perú.',
            'nivel': 'intermedio',
        },
        {
            'tipo': 'curso',
            'titulo': 'Plan de negocios y financiamiento para startups',
            'enlace': 'https://www.innovateperu.gob.pe/cursos/plan-negocios',
            'tematica': 'emprendimiento',
            'descripcion': 'Cómo elaborar un plan de negocios para conseguir inversionistas.',
            'nivel': 'avanzado',
        },
        
        # === PLANIFICACIÓN FINANCIERA ===
        {
            'tipo': 'video',
            'titulo': 'Metas financieras: Corto, mediano y largo plazo',
            'enlace': 'https://www.youtube.com/watch?v=ejemplo8',
            'tematica': 'planificacion',
            'descripcion': 'Cómo establecer y alcanzar tus objetivos financieros.',
            'nivel': 'principiante',
        },
        {
            'tipo': 'articulo',
            'titulo': 'Planificación para el retiro en Perú',
            'enlace': 'https://www.sbs.gob.pe/planificacion-jubilacion',
            'tematica': 'planificacion',
            'descripcion': 'Calcula cuánto necesitas ahorrar para tu jubilación.',
            'nivel': 'intermedio',
        },
        {
            'tipo': 'curso',
            'titulo': 'Asesoría financiera integral y patrimonial',
            'enlace': 'https://www.coursera.org/learn/planificacion-financiera',
            'tematica': 'planificacion',
            'descripcion': 'Curso completo sobre gestión patrimonial y planificación financiera.',
            'nivel': 'avanzado',
        },
        {
            'tipo': 'infografia',
            'titulo': 'Tu plan financiero en una página',
            'enlace': 'https://www.bbva.pe/infografia-plan-financiero',
            'tematica': 'planificacion',
            'descripcion': 'Plantilla visual para organizar todas tus finanzas.',
            'nivel': 'intermedio',
        },
    ]
    
    # Crear cada recurso
    for recurso_data in recursos:
        existe = RecursoAprendizaje.objects.filter(
            titulo=recurso_data['titulo']
        ).exists()
        
        if not existe:
            RecursoAprendizaje.objects.create(**recurso_data)


def eliminar_recursos_iniciales(apps, schema_editor):
    """Elimina los recursos iniciales (para rollback)"""
    RecursoAprendizaje = apps.get_model('aprendizaje', 'RecursoAprendizaje')
    
    titulos = [
        'Cómo hacer un presupuesto mensual efectivo',
        'Método 50/30/20 para distribuir tu sueldo',
        'Presupuesto familiar avanzado',
        'Introducción al ahorro: Primeros pasos',
        'Fondo de emergencia: ¿Cuánto necesitas?',
        '10 tips para ahorrar dinero todos los días',
        'Estrategias avanzadas de ahorro e inversión',
        '¿Qué es invertir? Conceptos básicos',
        'Inversión en la Bolsa de Valores de Lima',
        'Fondos mutuos y AFP en Perú',
        'Diversificación de cartera de inversiones',
        'Cómo salir de deudas: Método bola de nieve',
        'Refinanciamiento vs. Consolidación de deudas',
        'Señales de alerta: Sobreendeudamiento',
        'Historial crediticio: ¿Qué es y por qué importa?',
        'Tipos de créditos en el sistema financiero peruano',
        'Cómo negociar mejores tasas de interés',
        'Impuestos básicos en Perú: IGV y Renta',
        'Declaración anual de Impuesto a la Renta',
        'Planificación tributaria para profesionales independientes',
        'Cómo empezar un negocio con poco dinero',
        'Formalización de tu emprendimiento en Perú',
        'Casos de éxito: Emprendedores peruanos',
        'Plan de negocios y financiamiento para startups',
        'Metas financieras: Corto, mediano y largo plazo',
        'Planificación para el retiro en Perú',
        'Asesoría financiera integral y patrimonial',
        'Tu plan financiero en una página',
    ]
    
    RecursoAprendizaje.objects.filter(titulo__in=titulos).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('aprendizaje', '0002_initial'),  
    ]

    operations = [
        migrations.RunPython(
            crear_recursos_iniciales,
            eliminar_recursos_iniciales
        ),
    ]