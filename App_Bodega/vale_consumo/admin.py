from django.contrib import admin
from django.http import HttpResponse
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from .models import Unidad_Negocio, Centro_Costo, Bodega, Categoria, Recurso, Solicitud, Solicitud_Recurso, Personal
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

# PERSONAL
class PersonalAdmin(admin.ModelAdmin):
    list_display = (
        'id_persona',
        'nombre1_personal',
        'nombre2_personal',
        'apellido_p_personal',
        'apellido_m_personal',
        'is_active_personal'
    )
    search_fields = ['id_persona']

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
    readonly_fields = ('fecha_solicitud', 'hora_solicitud',)
    list_display = (
        'solicitante',
        'id_solicitud',
        'fecha_solicitud',
        'hora_solicitud',
        'unidad_negocio',
        'id_centro_costo',
        'piso',
        'retira',
        'preparador',
        'bodega',
        'estado_solicitud',
        'observacion',
        'is_active_solicitud'
    )
    fieldsets = (('Datos de la Solicitud',
                  {'fields':
                       (('solicitante', 'fecha_solicitud', 'hora_solicitud'),
                        ('id_centro_costo', 'unidad_negocio', 'piso', 'retira')),
                   'classes': 'collapse'}),
                 ('Asignaciones de la solicitud',
                  {'fields':
                       (('bodega', 'preparador'), ('estado_solicitud', 'observacion', 'is_active_solicitud')),
                   'classes': 'collapse wide'}),)
    resources_class = SolicitudResource

    actions = ['generar_pdf']

    def generar_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="solicitudes.pdf"'
        custom_size = (400,600)
        doc = SimpleDocTemplate(response, pagesize=custom_size)
        elements = []

        for solicitud in queryset:
            elements.append(Spacer(1, 10))  # Espacio entre solicitudes

            # Encabezado de la solicitud
            header = [
                ["Documento de salida N°: "+str(solicitud.id_solicitud)],
                ["Fecha y Hora: " + str(solicitud.fecha_solicitud) + " " + str(solicitud.hora_solicitud)],
                ["Unidad de Negocio: " + solicitud.unidad_negocio.nombre_unidad_negocio],
                ["Centro de Costo: " + solicitud.id_centro_costo.nombre_centro_costo],
                ["Bodega: " + solicitud.bodega.nombre_bodega],
                ["Piso: " + str(solicitud.piso)],
                ["Retira: " + str(solicitud.retira)],
                ["Preparador: " + str(solicitud.preparador)],
                ["Autoriza: " + solicitud.solicitante.first_name + " "+solicitud.solicitante.last_name ],
                ["Observaciones: " + solicitud.observacion],
                # Agrega más campos de Solicitud aquí
                # ...
            ]
            t = Table(header)
            t.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            elements.append(t)

            elements.append(Spacer(1, 5))  # Espacio entre encabezado y detalles

            # Detalles de recursos
            recursos_data = [
                ["Cod Rec","Recurso", "Unidad", "Cantidad"]
            ]
            for recurso in Solicitud_Recurso.objects.filter(id_solicitud=solicitud):
                recursos_data.append([recurso.id_recurso,recurso.id_recurso.nombre_recurso, recurso.id_recurso.unidad, str(recurso.cantidad_solicitada)])
            t_recursos = Table(recursos_data)
            t_recursos.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            elements.append(t_recursos)
            elements.append(Spacer(1, 5))  # Espacio entre encabezado y detalles
            footer = [
                ["Timbre y Firma entregado: "],
            ]
            t = Table(footer)
            t.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ]))
            elements.append(t)



            elements.append(PageBreak())  # Página nueva para la siguiente solicitud



        doc.build(elements)
        return response


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
admin.site.register(Personal, PersonalAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Recurso, RecursoAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(Solicitud_Recurso, Solicitud_RecursoAdmin)

