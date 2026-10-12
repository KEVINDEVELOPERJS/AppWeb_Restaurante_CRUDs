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

    def test_eliminar_mesa(self):
        respuesta = self.client.delete(f'/api/mesas/{self.mesa.id}/')
        self.assertEqual(respuesta.status_code, 204)
        self.assertFalse(Mesa.objects.filter(id=self.mesa.id).exists())

    def test_no_eliminar_zona_con_mesas(self):
        """Una Zona con Mesas no se borra y responde 400 con un mensaje claro."""
        respuesta = self.client.delete(f'/api/zonas/{self.zona.id}/')
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn('detail', respuesta.json())
        self.assertTrue(Zona.objects.filter(id=self.zona.id).exists())

    def test_eliminar_zona_sin_mesas(self):
        zona_vacia = Zona.objects.create(nombre='Terraza')
        respuesta = self.client.delete(f'/api/zonas/{zona_vacia.id}/')
        self.assertEqual(respuesta.status_code, 204)
        self.assertFalse(Zona.objects.filter(id=zona_vacia.id).exists())
