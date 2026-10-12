from rest_framework import viewsets, filters

from Pedidos.models import Pedido
from Pedidos.api.serializers import PedidoSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    # select_related trae la mesa y el plato en la misma consulta
    queryset = Pedido.objects.select_related('mesa', 'plato').all()
    serializer_class = PedidoSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['mesa__numero', 'plato__nombre', 'estado', 'observaciones']
