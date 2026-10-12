from rest_framework import serializers
from Platos.models import Plato
from ..models import Pedido


class PedidoSerializer(serializers.ModelSerializer):
    # Datos de solo lectura que vienen de los otros CRUDs (Mesas y Platos)
    zona = serializers.IntegerField(source='mesa.zona.id', read_only=True)
    zona_nombre = serializers.CharField(source='mesa.zona.nombre', read_only=True)
    mesa_numero = serializers.IntegerField(source='mesa.numero', read_only=True)
    categoria = serializers.IntegerField(source='plato.categoria.id', read_only=True)
    categoria_nombre = serializers.CharField(source='plato.categoria.nombre', read_only=True)
    plato_nombre = serializers.CharField(source='plato.nombre', read_only=True)
    precio_unitario = serializers.DecimalField(source='plato.precio', max_digits=10, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Pedido
        fields = [
            'id',
            'zona', 'zona_nombre',
            'mesa', 'mesa_numero',
            'categoria', 'categoria_nombre',
            'plato', 'plato_nombre', 'precio_unitario',
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
