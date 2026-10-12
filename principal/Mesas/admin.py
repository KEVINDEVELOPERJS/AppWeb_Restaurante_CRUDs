from django.contrib import admin
from .models import Mesa, Zona


@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa', 'creado_en')
    search_fields = ('nombre',)


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'zona', 'capacidad', 'estado', 'activa')
    list_filter = ('estado', 'activa', 'zona')
    search_fields = ('numero', 'zona__nombre')
