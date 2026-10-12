"""
Utilidades compartidas para los ViewSets de la API.

`ProtectedDeleteMixin` evita el error 500 que produce Django cuando se intenta
eliminar un registro referenciado por una ForeignKey con `on_delete=PROTECT`
(por ejemplo, una Categoría que tiene Platos o una Zona que tiene Mesas).

En su lugar devuelve un HTTP 400 con un mensaje entendible, que el frontend
muestra al usuario.
"""

from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.response import Response


class ProtectedDeleteMixin:
    """Traduce `ProtectedError` en un 400 con un mensaje claro en español."""

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError as error:
            return Response(
                {"detail": self._mensaje_protegido(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @staticmethod
    def _mensaje_protegido(error):
        """Arma un texto como: 'El registro está relacionado con 2 platos, 1 mesa; elimínalos o reasígnalos primero.'"""
        conteo = {}
        for obj in error.protected_objects:
            nombre = obj._meta.verbose_name_plural.lower()
            conteo[nombre] = conteo.get(nombre, 0) + 1

        if not conteo:
            return "El registro está en uso por otros registros."

        relaciones = ", ".join(
            f"{cantidad} {nombre}" for nombre, cantidad in conteo.items()
        )
        return (
            f"El registro está relacionado con {relaciones}; "
            "elimínalos o reasígnalos primero."
        )
