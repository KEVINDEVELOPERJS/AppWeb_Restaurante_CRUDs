from django.db import models
from django.core.validators import MinValueValidator

# Modelos de los compañeros con los que se relaciona el pedido
from Mesas.models import Mesa
from Platos.models import Plato


class Pedido(models.Model):
    """Pedido que hace una mesa del restaurante"""

    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        EN_PREPARACION = 'EN_PREPARACION', 'En preparación'
        ENTREGADO = 'ENTREGADO', 'Entregado'
        CANCELADO = 'CANCELADO', 'Cancelado'

    # Relaciones con Mesas y Platos (ForeignKey)
    mesa = models.ForeignKey(
        Mesa,
        on_delete=models.PROTECT,
        related_name='pedidos',
        help_text="Mesa que hace el pedido"
    )
    plato = models.ForeignKey(
        Plato,
        on_delete=models.PROTECT,
        related_name='pedidos',
        help_text="Plato que se pidió"
    )

    # Detalles
    cantidad = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Cuántas unidades del plato se pidieron"
    )
    observaciones = models.TextField(
        blank=True,
        null=True,
        help_text="Indicaciones para la cocina (ej: sin cebolla)"
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )

    # Auditoría
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-creado_en']

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.mesa.numero} - {self.plato.nombre} x{self.cantidad}"

    @property
    def total(self):
        """Precio del plato multiplicado por la cantidad"""
        return self.plato.precio * self.cantidad
