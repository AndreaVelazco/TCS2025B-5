from django.test import TestCase
from rest_framework.test import APIClient
from usuarios.models import Usuario


class EvaluacionesAPITest(TestCase):
	def setUp(self):
		self.client = APIClient()
		# crear usuario (create_user espera correo, nombre, password)
		self.user = Usuario.objects.create_user(correo='t@test.com', nombre='Tester', password='testpass')
		# autenticación - usar endpoint token (nuestro CustomTokenObtainPair acepta 'usuario' como alias)
		resp = self.client.post('/api/token/', {'usuario': 't@test.com', 'password': 'testpass'}, format='json')
		self.assertEqual(resp.status_code, 200)
		self.access = resp.data['access']
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)

	def test_create_question_and_answer(self):
		# crear pregunta con opciones como lista de objetos indicando la correcta
		payload = {
			'categoria': 'ahorro',
			'pregunta': '¿Cuál es la mejor forma de ahorrar?',
			'opciones': [
				{'texto': 'Guardar en casa', 'correcta': False},
				{'texto': 'Depositar en banco', 'correcta': True},
				{'texto': 'Invertir en risk', 'correcta': False}
			],
			'nivel_dificultad': 'facil'
		}
		# usar la ruta de preguntas: /api/evaluaciones/preguntas/
		resp = self.client.post('/api/evaluaciones/preguntas/', payload, format='json')
		self.assertIn(resp.status_code, (201, 200))
		qid = resp.data.get('id_pregunta')
		self.assertIsNotNone(qid)

		# responder la pregunta
		respuestas_payload = {
			'respuestas': [
				{'pregunta_id': qid, 'respuesta': 1}
			]
		}
		resp2 = self.client.post('/api/evaluaciones/tests/enviar_respuestas/', respuestas_payload, format='json')
		self.assertEqual(resp2.status_code, 201)
		self.assertIn('puntuacion_total', resp2.data)
