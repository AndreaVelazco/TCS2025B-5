from django.db import migrations
import json

def crear_preguntas_iniciales(apps, schema_editor):
    """Crea las preguntas del minitest inicial"""
    PreguntaTest = apps.get_model('evaluaciones', 'PreguntaTest')
    
    preguntas = [
        # === PRESUPUESTO (5 preguntas) ===
        {
            'categoria': 'presupuesto',
            'pregunta': '¿Con qué frecuencia revisas tus gastos mensuales?',
            'opciones': json.dumps([
                'Nunca lo hago',
                'De vez en cuando',
                'Mensualmente',
                'Semanalmente'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Revisar tus gastos semanalmente te permite tener un mejor control y ajustar tu presupuesto a tiempo.',
            'nivel_dificultad': 'facil',
            'activa': True,
        },
        {
            'categoria': 'presupuesto',
            'pregunta': '¿Utilizas alguna herramienta o aplicación para controlar tu presupuesto?',
            'opciones': json.dumps([
                'No uso nada',
                'Solo anoto mentalmente',
                'Uso Excel o cuaderno',
                'Uso una app especializada'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Las apps especializadas te ayudan a automatizar el seguimiento y obtener reportes detallados.',
            'nivel_dificultad': 'facil',
            'activa': True,
        },
        {
            'categoria': 'presupuesto',
            'pregunta': '¿Qué porcentaje de tu sueldo destinas a gastos esenciales (vivienda, comida, transporte)?',
            'opciones': json.dumps([
                'Más del 80%',
                'Entre 60-80%',
                'Entre 40-60%',
                'Menos del 40%'
            ]),
            'respuesta_correcta': 1,
            'explicacion': 'Lo ideal es destinar entre 50-60% a necesidades básicas según la regla 50/30/20.',
            'nivel_dificultad': 'medio',
            'activa': True,
        },
        {
            'categoria': 'presupuesto',
            'pregunta': '¿Tienes gastos hormiga (pequeñas compras diarias) que sumes y controles?',
            'opciones': json.dumps([
                'No sé qué son gastos hormiga',
                'No los controlo',
                'Los controlo ocasionalmente',
                'Los registro todos'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Los gastos hormiga pueden representar hasta 20% de tu presupuesto si no los controlas.',
            'nivel_dificultad': 'medio',
            'activa': True,
        },
        {
            'categoria': 'presupuesto',
            'pregunta': '¿Planificas tus gastos grandes (electrodomésticos, viajes) con anticipación?',
            'opciones': json.dumps([
                'Nunca, compro cuando lo necesito',
                'A veces ahorro un poco',
                'Sí, ahorro mensualmente para eso',
                'Sí, y tengo un fondo específico para imprevistos'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Planificar gastos grandes evita el endeudamiento y te permite conseguir mejores precios.',
            'nivel_dificultad': 'medio',
            'activa': True,
        },
        
        # === AHORRO (5 preguntas) ===
        {
            'categoria': 'ahorro',
            'pregunta': '¿Ahorras dinero de manera regular?',
            'opciones': json.dumps([
                'No ahorro nada',
                'Solo cuando me sobra',
                'Ahorro ocasionalmente',
                'Ahorro mensualmente un monto fijo'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'El ahorro debe ser automático y prioritario, no lo que sobra al final del mes.',
            'nivel_dificultad': 'facil',
            'activa': True,
        },
        {
            'categoria': 'ahorro',
            'pregunta': '¿Tienes un fondo de emergencia para imprevistos?',
            'opciones': json.dumps([
                'No tengo nada ahorrado',
                'Tengo menos de 1 mes de gastos',
                'Tengo entre 1-3 meses de gastos',
                'Tengo más de 3 meses de gastos'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Lo recomendable es tener de 3 a 6 meses de gastos en tu fondo de emergencia.',
            'nivel_dificultad': 'medio',
            'activa': True,
        },
        {
            'categoria': 'ahorro',
            'pregunta': '¿Qué porcentaje de tu ingreso mensual ahorras?',
            'opciones': json.dumps([
                'No ahorro (0%)',
                'Menos del 10%',
                'Entre 10-20%',
                'Más del 20%'
            ]),
            'respuesta_correcta': 2,
            'explicacion': 'Se recomienda ahorrar al menos el 20% de tus ingresos según la regla 50/30/20.',
            'nivel_dificultad': 'medio',
            'activa': True,
        },
        {
            'categoria': 'ahorro',
            'pregunta': '¿Dónde guardas tus ahorros?',
            'opciones': json.dumps([
                'En efectivo en casa',
                'En cuenta de ahorros sin intereses',
                'En cuenta de ahorros con intereses',
                'Diversificado: banco, inversiones, etc.'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Diversificar tus ahorros te protege contra la inflación y maximiza rendimientos.',
            'nivel_dificultad': 'medio',
            'activa': True,
        },
        {
            'categoria': 'ahorro',
            'pregunta': '¿Tienes metas claras de ahorro (viaje, casa, educación)?',
            'opciones': json.dumps([
                'No tengo metas definidas',
                'Tengo ideas vagas',
                'Tengo metas pero sin plazos',
                'Tengo metas específicas con plazos y montos'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Las metas SMART (específicas, medibles, alcanzables, relevantes y temporales) aumentan tu éxito.',
            'nivel_dificultad': 'facil',
            'activa': True,
        },
        
        # === INVERSIÓN (5 preguntas) ===
        {
            'categoria': 'inversion',
            'pregunta': '¿Has invertido dinero alguna vez?',
            'opciones': json.dumps([
                'Nunca he invertido',
                'He pensado en invertir',
                'Tengo pequeñas inversiones',
                'Invierto regularmente'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Invertir regularmente aprovecha el poder del interés compuesto a largo plazo.',
            'nivel_dificultad': 'facil',
            'activa': True,
        },
        {
            'categoria': 'inversion',
            'pregunta': '¿Conoces la diferencia entre renta fija y renta variable?',
            'opciones': json.dumps([
                'No sé qué son',
                'He escuchado los términos',
                'Sé lo básico',
                'Los entiendo y puedo explicarlos'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Renta fija (bonos) ofrece ingresos predecibles; renta variable (acciones) tiene mayor potencial pero más riesgo.',
            'nivel_dificultad': 'medio',
            'activa': True,
        },
        {
            'categoria': 'inversion',
            'pregunta': '¿Cuál es tu tolerancia al riesgo en inversiones?',
            'opciones': json.dumps([
                'Prefiero no arriesgar nada',
                'Solo riesgo mínimo',
                'Riesgo moderado',
                'Puedo asumir alto riesgo por mayores ganancias'
            ]),
            'respuesta_correcta': 2,
            'explicacion': 'El riesgo moderado balances seguridad y crecimiento, ideal para la mayoría de inversionistas.',
            'nivel_dificultad': 'medio',
            'activa': True,
        },
        {
            'categoria': 'inversion',
            'pregunta': '¿Conoces qué es la diversificación de inversiones?',
            'opciones': json.dumps([
                'No sé qué es',
                'He escuchado del tema',
                'Sé el concepto básico',
                'Lo aplico en mis inversiones'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Diversificar reduce el riesgo al no poner "todos los huevos en una sola canasta".',
            'nivel_dificultad': 'dificil',
            'activa': True,
        },
        {
            'categoria': 'inversion',
            'pregunta': '¿Con qué frecuencia revisas tus inversiones?',
            'opciones': json.dumps([
                'No tengo inversiones',
                'Casi nunca las reviso',
                'Cada 6 meses o anualmente',
                'Mensualmente o trimestralmente'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Revisar trimestralmente permite ajustar tu estrategia sin caer en especulación diaria.',
            'nivel_dificultad': 'medio',
            'activa': True,
        },
        
        # === DEUDAS (5 preguntas) ===
        {
            'categoria': 'deudas',
            'pregunta': '¿Tienes deudas actualmente?',
            'opciones': json.dumps([
                'Sí, muchas y no las controlo',
                'Sí, algunas que voy pagando',
                'Solo deudas menores',
                'No tengo deudas'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'No tener deudas o mantenerlas bajo control es clave para la salud financiera.',
            'nivel_dificultad': 'facil',
            'activa': True,
        },
        {
            'categoria': 'deudas',
            'pregunta': '¿Qué porcentaje de tu ingreso mensual destinas a pagar deudas?',
            'opciones': json.dumps([
                'Más del 40%',
                'Entre 30-40%',
                'Entre 10-30%',
                'Menos del 10% o nada'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Lo ideal es que las deudas no superen el 30% de tus ingresos mensuales.',
            'nivel_dificultad': 'medio',
            'activa': True,
        },
        {
            'categoria': 'deudas',
            'pregunta': '¿Conoces las tasas de interés de tus deudas actuales?',
            'opciones': json.dumps([
                'No sé cuánto pago de interés',
                'Tengo una idea vaga',
                'Sé la tasa de algunas',
                'Conozco todas mis tasas de interés'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Conocer tus tasas te permite priorizar qué deudas pagar primero (las de mayor interés).',
            'nivel_dificultad': 'medio',
            'activa': True,
        },
        {
            'categoria': 'deudas',
            'pregunta': '¿Has refinanciado alguna deuda para obtener mejores condiciones?',
            'opciones': json.dumps([
                'No sé qué es refinanciar',
                'Lo he considerado pero no lo he hecho',
                'Sí, una vez',
                'Sí, lo hago cuando conviene'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Refinanciar puede reducir intereses y cuotas, liberando flujo de efectivo.',
            'nivel_dificultad': 'dificil',
            'activa': True,
        },
        {
            'categoria': 'deudas',
            'pregunta': '¿Usas tu tarjeta de crédito de manera responsable?',
            'opciones': json.dumps([
                'No tengo tarjeta',
                'La uso y a veces pago el mínimo',
                'Pago más del mínimo pero no todo',
                'Siempre pago el total antes del vencimiento'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Pagar el total evita intereses y mantiene tu historial crediticio limpio.',
            'nivel_dificultad': 'medio',
            'activa': True,
        },
        
        # === CRÉDITO (5 preguntas) ===
        {
            'categoria': 'credito',
            'pregunta': '¿Conoces tu historial crediticio o score crediticio?',
            'opciones': json.dumps([
                'No sé qué es',
                'He escuchado pero no lo he revisado',
                'Lo revisé hace tiempo',
                'Lo reviso regularmente'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Revisar tu score regularmente te permite corregir errores y mejorar tu perfil crediticio.',
            'nivel_dificultad': 'facil',
            'activa': True,
        },
        {
            'categoria': 'credito',
            'pregunta': '¿Sabes cómo mejorar tu calificación crediticia?',
            'opciones': json.dumps([
                'No tengo idea',
                'Algo he escuchado',
                'Conozco algunos factores',
                'Sé qué hacer y lo aplico activamente'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Pagar a tiempo, mantener baja utilización de crédito y diversificar tipos de crédito mejora tu score.',
            'nivel_dificultad': 'medio',
            'activa': True,
        },
        {
            'categoria': 'credito',
            'pregunta': '¿Pagas tus facturas y créditos a tiempo?',
            'opciones': json.dumps([
                'Frecuentemente me atraso',
                'A veces me atraso',
                'Casi siempre pago a tiempo',
                'Siempre pago antes o en la fecha'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'El historial de pagos representa el 35% de tu score crediticio.',
            'nivel_dificultad': 'facil',
            'activa': True,
        },
        {
            'categoria': 'credito',
            'pregunta': '¿Cuántas tarjetas de crédito tienes?',
            'opciones': json.dumps([
                'Ninguna',
                '1-2 tarjetas',
                '3-4 tarjetas',
                'Más de 4 tarjetas'
            ]),
            'respuesta_correcta': 1,
            'explicacion': 'Tener 1-2 tarjetas bien manejadas es suficiente y más fácil de controlar.',
            'nivel_dificultad': 'facil',
            'activa': True,
        },
        {
            'categoria': 'credito',
            'pregunta': '¿Entiendes los términos de tu contrato de crédito (TEA, TCEA, seguros)?',
            'opciones': json.dumps([
                'No los entiendo',
                'Entiendo algo',
                'Entiendo lo básico',
                'Los comprendo totalmente y comparo antes de firmar'
            ]),
            'respuesta_correcta': 3,
            'explicacion': 'Entender la TCEA (Tasa de Costo Efectivo Anual) te permite comparar el costo real de créditos.',
            'nivel_dificultad': 'dificil',
            'activa': True,
        },
    ]
    
    # Crear cada pregunta
    for pregunta_data in preguntas:
        existe = PreguntaTest.objects.filter(
            pregunta=pregunta_data['pregunta']
        ).exists()
        
        if not existe:
            PreguntaTest.objects.create(**pregunta_data)


def eliminar_preguntas_iniciales(apps, schema_editor):
    """Elimina las preguntas iniciales (para rollback)"""
    PreguntaTest = apps.get_model('evaluaciones', 'PreguntaTest')
    
    # Eliminar por categorías para estar seguros
    PreguntaTest.objects.filter(
        categoria__in=['presupuesto', 'ahorro', 'inversion', 'deudas', 'credito']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('evaluaciones', '0002_initial'),  
    ]

    operations = [
        migrations.RunPython(
            crear_preguntas_iniciales,
            eliminar_preguntas_iniciales
        ),
    ]