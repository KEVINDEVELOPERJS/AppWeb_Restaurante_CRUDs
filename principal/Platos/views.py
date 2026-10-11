from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from Platos.models import Plato, Categoria
from Platos.api.serializers import (
    PlatoSerializer,
    PlatoListSerializer,
    CategoriaSerializer,
)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']


class PlatoViewSet(viewsets.ModelViewSet):
    queryset = Plato.objects.select_related('categoria').all()
    serializer_class = PlatoSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion', 'categoria__nombre']
    ordering_fields = ['precio', 'nombre', 'creado_en']
    ordering = ['-destacado', 'nombre']

    def get_serializer_class(self):
        if self.action == 'list':
            return PlatoListSerializer
        return PlatoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get('estado')
        categoria = self.request.query_params.get('categoria')
        destacado = self.request.query_params.get('destacado')

        if estado:
            queryset = queryset.filter(estado=estado)
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
        if destacado is not None:
            queryset = queryset.filter(destacado=destacado.lower() == 'true')

        return queryset

    @action(detail=False, methods=['get'])
    def destacados(self, request):
        platos = self.get_queryset().filter(destacado=True, estado=Plato.Estado.DISPONIBLE)
        serializer = PlatoListSerializer(platos, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        plato = self.get_object()
        nuevo_estado = request.data.get('estado')
        if nuevo_estado not in dict(Plato.Estado.choices):
            return Response({'error': 'Estado no válido'}, status=status.HTTP_400_BAD_REQUEST)
        plato.estado = nuevo_estado
        plato.save()
        return Response(PlatoSerializer(plato).data)