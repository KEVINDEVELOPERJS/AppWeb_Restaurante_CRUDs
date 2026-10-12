from django.test import TestCase
from rest_framework.test import APIClient

from Platos.models import Categoria, Plato


class CategoriasApiTests(TestCase):
    """Pruebas del CRUD de Categorías, en especial la eliminación."""

    def setUp(self):
        self.client = APIClient()
        self.categoria = Categoria.objects.create(nombre='Entradas')

    def test_no_eliminar_categoria_con_platos(self):
        """Una Categoría con Platos no se borra y responde 400 con un mensaje claro."""
        Plato.objects.create(nombre='Ensalada', categoria=self.categoria, precio='5.00')
        respuesta = self.client.delete(f'/api/categorias/{self.categoria.id}/')
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn('detail', respuesta.json())
        self.assertTrue(Categoria.objects.filter(id=self.categoria.id).exists())

    def test_eliminar_categoria_sin_platos(self):
        respuesta = self.client.delete(f'/api/categorias/{self.categoria.id}/')
        self.assertEqual(respuesta.status_code, 204)
        self.assertFalse(Categoria.objects.filter(id=self.categoria.id).exists())
