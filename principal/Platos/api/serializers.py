from rest_framework import serializers
from ..models import Plato, Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'activa', 'creado_en']
        read_only_fields = ['id', 'creado_en']


class PlatoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    margen_ganancia = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Plato
        fields = [
            'id', 'nombre', 'descripcion',
            'categoria', 'categoria_nombre',
            'precio', 'precio_costo', 'margen_ganancia',
            'imagen', 'tiempo_preparacion', 'calorias',
            'es_vegetariano', 'es_picante',
            'estado', 'destacado',
            'creado_en', 'actualizado_en',
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a cero.")
        return value

    def validate(self, data):
        precio = data.get('precio', getattr(self.instance, 'precio', None))
        precio_costo = data.get('precio_costo', getattr(self.instance, 'precio_costo', 0))
        if precio and precio_costo and precio_costo > precio:
            raise serializers.ValidationError({
                'precio_costo': 'El costo no puede ser mayor que el precio de venta.'
            })
        return data


class PlatoListSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Plato
        fields = ['id', 'nombre', 'categoria_nombre', 'precio', 'estado', 'destacado', 'imagen']