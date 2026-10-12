from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Mesas.models import Mesa, Zona
from Mesas.api.serializers import (
    MesaSerializer,
    MesaListSerializer,
    ZonaSerializer,
)


class ZonaViewSet(viewsets.ModelViewSet):
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']


class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.select_related('zona').all()
    serializer_class = MesaSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['numero', 'descripcion', 'zona__nombre']
    ordering_fields = ['numero', 'capacidad', 'creado_en']
    ordering = ['numero']

    def get_serializer_class(self):
        if self.action == 'list':
            return MesaListSerializer
        return MesaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get('estado')
        zona = self.request.query_params.get('zona')

        if estado:
            queryset = queryset.filter(estado=estado)
        if zona:
            queryset = queryset.filter(zona_id=zona)

        return queryset

    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        mesas = self.get_queryset().filter(estado=Mesa.Estado.DISPONIBLE, activa=True)
        serializer = MesaListSerializer(mesas, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        mesa = self.get_object()
        nuevo_estado = request.data.get('estado')
        if nuevo_estado not in dict(Mesa.Estado.choices):
            return Response({'error': 'Estado no válido'}, status=status.HTTP_400_BAD_REQUEST)
        mesa.estado = nuevo_estado
        mesa.save()
        return Response(MesaSerializer(mesa).data)
