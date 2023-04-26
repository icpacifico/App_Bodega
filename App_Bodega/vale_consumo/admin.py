from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Unidad_Negocio, Centro_Costo, Bodega, Categoria, Recurso, Solicitud, Solicitud_Recurso
from usuario.models import UserProfile  # Preparador,


# Register your models here.


# IMPORT - EXPORT
class Unidad_NegocioResource(resources.ModelResource):
    class Meta:
        model: Unidad_Negocio


class Centro_CostoResource(resources.ModelResource):
    class Meta:
        model = Centro_Costo


class CategoriaResource(resources.ModelResource):
    class Meta:
        model = Categoria


class RecursoResource(resources.ModelResource):
    class Meta:
        model = Recurso


class SolicitudResource(resources.ModelResource):
    class Meta:
        model = Solicitud


class Solicitud_RecursoResource(resources.ModelResource):
    class Meta:
        model = Solicitud_Recurso


# UNIDAD DE NEGOCIO
class Unidad_NegocioAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_unidad_negocio',
        'is_active_unidad_negocio'
    )
    search_fields = ['id']
    resources_class = Unidad_NegocioResource


# CENTRO DE COSTOS
class Cetro_CostoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'unidad_negocio',
        'crr',
        'nombre_centro_costo',
        'g_part',
        'cc',
        'comentario',
        'is_active_centro_costo'
    )
    search_fields = ['id_centro_costo']
    resources_class = Centro_CostoResource


# BODEGA
class BodegaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_bodega',
        'is_active_bodega'
    )
    search_fields = ['id']


# CATEGORIA
class CategoriaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_categoria',
        'is_active_categoria'
    )
    resources_class = CategoriaResource


# RECURSO
class RecursoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'id',
        'categoria_recurso',
        'nombre_recurso',
        'unidad',
        'is_active_recurso'
    )
    search_fields = ['id', 'nombre_recurso']
    resources_class = RecursoResource
# SOLICITUD RECURSO INLINE


class Solicitud_RecursoInline(admin.TabularInline):
    model = Solicitud_Recurso
    extra = 2
    search_fields = ['id_recurso']
    autocomplete_fields = ['id_recurso']


# SOLICITUD
class SolicitudAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    search_fields = ['id_centro_costo', 'bodega']
    autocomplete_fields = ['id_centro_costo', 'bodega']
    inlines = [Solicitud_RecursoInline, ]
    list_display = (
        'solicitante',
        'id_solicitud',
        'fecha_solicitud',
        'hora_solicitud',
        'unidad_negocio',
        'id_centro_costo',
        'piso',
        'preparador',
        'bodega',
        'estado_solicitud',
        'observacion',
        'is_active_solicitud'
    )
    fieldsets = (('Datos de la Solicitud',
                  {'fields':
                       (('solicitante', 'fecha_solicitud', 'hora_solicitud'),
                        ('id_centro_costo', 'unidad_negocio', 'piso')),
                   'classes': 'collapse'}),
                 ('Asignaciones de la solicitud',
                  {'fields':
                       (('bodega', 'preparador'), ('estado_solicitud', 'observacion', 'is_active_solicitud')),
                   'classes': 'collapse wide'}),)
    resources_class = SolicitudResource


"""class SolicitudAdmin(admin.ModelAdmin):
    exclude = ('is_active_solicitud',)"""


# SOLICITUD RECURSO
class Solicitud_RecursoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'id_solicitud_recurso',
        'id_solicitud',
        'id_recurso',
        'cantidad_solicitada',
        'estado_despacho'
    )
    resources_class = Solicitud_RecursoResource


admin.site.register(Unidad_Negocio, Unidad_NegocioAdmin)
admin.site.register(Centro_Costo, Cetro_CostoAdmin)
admin.site.register(Bodega, BodegaAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Recurso, RecursoAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(Solicitud_Recurso, Solicitud_RecursoAdmin)

