from django.test import TestCase
from rest_framework.test import APIClient

from Mesas.models import Mesa, Zona


class MesasApiTests(TestCase):
    """Pruebas básicas del CRUD de Mesas (GET y POST)."""

    def setUp(self):
        self.client = APIClient()
        self.zona = Zona.objects.create(nombre='Salón')
        self.mesa = Mesa.objects.create(numero=1, zona=self.zona, capacidad=4)

    def test_listar_mesas(self):
        respuesta = self.client.get('/api/mesas/')
        self.assertEqual(respuesta.status_code, 200)

    def test_crear_mesa(self):
        datos = {'numero': 2, 'zona': self.zona.id, 'capacidad': 2}
        respuesta = self.client.post('/api/mesas/', datos, format='json')
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(Mesa.objects.count(), 2)

    def test_listar_zonas(self):
        respuesta = self.client.get('/api/zonas/')
        self.assertEqual(respuesta.status_code, 200)
