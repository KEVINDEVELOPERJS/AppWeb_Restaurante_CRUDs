from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Categoria(models.Model):
    """Categoría a la que pertenece un plato (ej: Entradas, Platos fuertes, Postres)"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Plato(models.Model):
    """Modelo principal para los platos del restaurante"""

    class Estado(models.TextChoices):
        DISPONIBLE = 'DISPONIBLE', 'Disponible'
        AGOTADO = 'AGOTADO', 'Agotado'
        DESCONTINUADO = 'DESCONTINUADO', 'Descontinuado'

    # Información básica
    nombre = models.CharField(
        max_length=150,
        unique=True,
        help_text="Nombre del plato"
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        help_text="Descripción detallada del plato"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='platos',
        help_text="Categoría del plato"
    )

    # Precios
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Precio de venta en pesos"
    )
    precio_costo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0'))],
        help_text="Costo de preparación (opcional)"
    )

    # Imagen
    imagen = models.ImageField(
        upload_to='platos/',
        blank=True,
        null=True,
        help_text="Imagen del plato"
    )

    # Detalles
    tiempo_preparacion = models.PositiveIntegerField(
        default=15,
        validators=[MinValueValidator(1), MaxValueValidator(180)],
        help_text="Tiempo de preparación en minutos"
    )
    calorias = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Calorías aproximadas"
    )
    es_vegetariano = models.BooleanField(default=False)
    es_picante = models.BooleanField(default=False)

    # Estado y control
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.DISPONIBLE
    )
    destacado = models.BooleanField(
        default=False,
        help_text="Mostrar en sección de destacados"
    )

    # Auditoría
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Plato"
        verbose_name_plural = "Platos"
        ordering = ['-destacado', 'nombre']
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['categoria']),
        ]

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

    @property
    def margen_ganancia(self):
        """Calcula el margen de ganancia"""
        if self.precio_costo and self.precio_costo > 0:
            return self.precio - self.precio_costo
        return None

    @property
    def disponible(self):
        """Retorna True si el plato está disponible"""
        return self.estado == self.Estado.DISPONIBLE