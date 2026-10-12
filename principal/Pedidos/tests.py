from django.test import TestCase
from rest_framework.test import APIClient

from Mesas.models import Mesa, Zona
from Platos.models import Plato, Categoria
from Pedidos.models import Pedido


class PedidosApiTests(TestCase):
    """Pruebas básicas del CRUD de Pedidos."""

    def setUp(self):
        self.client = APIClient()
        zona = Zona.objects.create(nombre='Salón')
        categoria = Categoria.objects.create(nombre='Platos fuertes')
        self.mesa = Mesa.objects.create(numero=1, zona=zona, capacidad=4)
        self.plato = Plato.objects.create(nombre='Bandeja Paisa', categoria=categoria, precio=35000)

    def test_listar_pedidos(self):
        respuesta = self.client.get('/api/pedidos/')
        self.assertEqual(respuesta.status_code, 200)

    def test_crear_pedido(self):
        datos = {'mesa': self.mesa.id, 'plato': self.plato.id, 'cantidad': 2}
        respuesta = self.client.post('/api/pedidos/', datos, format='json')
        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(Pedido.objects.count(), 1)
        self.assertEqual(respuesta.data['total'], '70000.00')

    def test_no_permite_plato_agotado(self):
        self.plato.estado = Plato.Estado.AGOTADO
        self.plato.save()
        datos = {'mesa': self.mesa.id, 'plato': self.plato.id, 'cantidad': 1}
        respuesta = self.client.post('/api/pedidos/', datos, format='json')
        self.assertEqual(respuesta.status_code, 400)
