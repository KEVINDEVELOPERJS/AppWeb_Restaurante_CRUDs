from django.contrib import admin
from .models import Pedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'mesa', 'plato', 'cantidad', 'estado', 'creado_en')
    list_filter = ('estado',)
