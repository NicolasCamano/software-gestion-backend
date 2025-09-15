# gestion/admin.py

from django.contrib import admin
# 1. Importa Recaudacion junto a los otros modelos
from .models import SalaJuegos, Maquina, Recaudacion, RegistroInventario,  Mantenimiento

# 2. Registra el nuevo modelo
admin.site.register(SalaJuegos)
admin.site.register(Maquina)
admin.site.register(Recaudacion)
admin.site.register(RegistroInventario)
@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('maquina', 'tecnico', 'fecha', 'descripcion')
    list_filter = ('maquina', 'tecnico', 'fecha')
    search_fields = ('descripcion',)
    ordering = ('-fecha',)