from rest_framework import serializers
from ..models import Mesa, Zona


class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = ['id', 'nombre', 'descripcion', 'activa', 'creado_en']
        read_only_fields = ['id', 'creado_en']


class MesaSerializer(serializers.ModelSerializer):
    zona_nombre = serializers.CharField(source='zona.nombre', read_only=True)

    class Meta:
        model = Mesa
        fields = [
            'id', 'numero', 'descripcion',
            'zona', 'zona_nombre',
            'capacidad', 'estado', 'activa',
            'creado_en', 'actualizado_en',
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']

    def validate_capacidad(self, value):
        if value < 1:
            raise serializers.ValidationError("La capacidad debe ser de al menos 1 persona.")
        return value


class MesaListSerializer(serializers.ModelSerializer):
    zona_nombre = serializers.CharField(source='zona.nombre', read_only=True)

    class Meta:
        model = Mesa
        fields = ['id', 'numero', 'zona_nombre', 'capacidad', 'estado', 'activa']
