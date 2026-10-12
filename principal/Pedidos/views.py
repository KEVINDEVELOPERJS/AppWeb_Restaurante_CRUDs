from rest_framework import viewsets, filters

from Pedidos.models import Pedido
from Pedidos.api.serializers import PedidoSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    # select_related trae la mesa (con su zona) y el plato (con su categoría) en la misma consulta
    queryset = Pedido.objects.select_related('mesa__zona', 'plato__categoria').all()
    serializer_class = PedidoSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['mesa__numero', 'mesa__zona__nombre', 'plato__nombre', 'plato__categoria__nombre', 'estado']
