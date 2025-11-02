from django.test import TestCase
from rest_framework.test import APIClient
from .models import Usuario


class AuthTokenTest(TestCase):
	def setUp(self):
		# Crear usuario de prueba
		self.user = Usuario.objects.create_user(
			correo='test@example.com', nombre='Test User', password='password123'
		)
		self.client = APIClient()

	def test_obtain_token_with_usuario_and_access_protected(self):
		# Solicitar tokens usando el campo 'usuario'
		resp = self.client.post('/api/token/', {'usuario': 'test@example.com', 'password': 'password123'}, format='json')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('access', resp.data)
		self.assertIn('refresh', resp.data)

		# Acceder a un endpoint protegido usando el token
		access = resp.data['access']
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
		resp2 = self.client.get('/api/finanzas/registros/')
		# Debería devolver 200 y una lista (posible lista vacía)
		self.assertEqual(resp2.status_code, 200)
