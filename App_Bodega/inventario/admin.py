from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Familia, Inventario, Detalle_Inventario
# Register your models here.


class FamiliaAdmin(admin.ModelAdmin):
    list_display = (
        'id_familia',
        'nombre_familia',
        'is_active'
    )
    search_fields = ['id_familia','nombre_familia','is_active']

class Detalle_InventarioInline(admin.TabularInline):
    model = Detalle_Inventario
    extra = 2
    search_fields = ['id_recurso']

class InventarioAdmin(admin.ModelAdmin):
    inlines = [Detalle_InventarioInline]
    list_display = (
        'id_inventaro',
        'fecha_inventario',
        'is_active_inventario'
    )
class Detalle_InventarioAdmin(admin.ModelAdmin):
    list_display = (
        'id_detalle_inventario',
        'no_inventario',
        'recurso_inventariado',
        'cantidad_inventariada'
    )

admin.site.register(Familia, FamiliaAdmin)
admin.site.register(Inventario, InventarioAdmin)
admin.site.register(Detalle_Inventario, Detalle_InventarioAdmin)
