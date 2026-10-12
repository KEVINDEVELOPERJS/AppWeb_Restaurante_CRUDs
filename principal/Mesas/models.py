from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Zona(models.Model):
    """Zona o área del restaurante donde se ubican las mesas (ej: Salón, Terraza, VIP)"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Zona"
        verbose_name_plural = "Zonas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Mesa(models.Model):
    """Modelo principal para las mesas del restaurante"""

    class Estado(models.TextChoices):
        DISPONIBLE = 'DISPONIBLE', 'Disponible'
        OCUPADA = 'OCUPADA', 'Ocupada'
        RESERVADA = 'RESERVADA', 'Reservada'
        MANTENIMIENTO = 'MANTENIMIENTO', 'En mantenimiento'

    # Información básica
    numero = models.PositiveIntegerField(
        unique=True,
        validators=[MinValueValidator(1)],
        help_text="Número que identifica la mesa"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción o nota de la mesa"
    )

    # Relación con la zona del restaurante (ForeignKey)
    zona = models.ForeignKey(
        Zona,
        on_delete=models.PROTECT,
        related_name='mesas',
        help_text="Zona del restaurante donde se ubica la mesa"
    )

    # Detalles
    capacidad = models.PositiveIntegerField(
        default=2,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        help_text="Cantidad de personas que caben en la mesa"
    )

    # Estado y control
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.DISPONIBLE
    )
    activa = models.BooleanField(
        default=True,
        help_text="Indica si la mesa está habilitada"
    )

    # Auditoría
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        ordering = ['numero']
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['zona']),
        ]

    def __str__(self):
        return f"Mesa {self.numero} - {self.zona.nombre} ({self.capacidad} personas)"

    @property
    def disponible(self):
        """Retorna True si la mesa está disponible"""
        return self.estado == self.Estado.DISPONIBLE
