from rest_framework import serializers
from Platos.models import Plato
from ..models import Pedido


class PedidoSerializer(serializers.ModelSerializer):
    # Campos de solo lectura para mostrar datos de Mesa y Plato en la tabla
    mesa_numero = serializers.IntegerField(source='mesa.numero', read_only=True)
    plato_nombre = serializers.CharField(source='plato.nombre', read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Pedido
        fields = [
            'id',
            'mesa', 'mesa_numero',
            'plato', 'plato_nombre',
            'cantidad', 'total',
            'observaciones', 'estado',
            'creado_en', 'actualizado_en',
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']

    def validate_plato(self, value):
        # Si se está editando y el plato no cambió, se deja pasar
        if self.instance and self.instance.plato == value:
            return value
        if value.estado != Plato.Estado.DISPONIBLE:
            raise serializers.ValidationError("Este plato no está disponible en este momento.")
        return value
