from django.db import models
from django.forms import model_to_dict
from usuario.models import UserProfile  # , Preparador
from django.contrib.auth.models import User

is_active = 'Activo'
is_inactive = 'Inactivo'

IS_ACTIVE_CHOICES = [(is_active, 'Activo'),
                     (is_inactive, 'Inactivo'), ]


# MODELO: UNIDAD DE NEGOCIO
class Unidad_Negocio(models.Model):
    # id_unidad_negocio = models.AutoField(primary_key=True)
    nombre_unidad_negocio = models.CharField(max_length=100, blank=False, null=False)
    is_active_unidad_negocio = models.CharField(max_length=10, blank=False, null=False, choices=IS_ACTIVE_CHOICES,
                                                default=is_active)

    def __str__(self):
        return self.nombre_unidad_negocio

    class Meta:
        verbose_name = "Unidad de Negocio"
        verbose_name_plural = "Unidades de Negocios"


# MODELO: CENTRO DE COSTOS
class Centro_Costo(models.Model):
    # id_centro_costo = models.AutoField(primary_key=True)
    nombre_centro_costo = models.CharField(max_length=100, blank=False, null=False)
    crr = models.IntegerField(blank=False, null=False)
    g_part = models.CharField(max_length=100, blank=False, null=False)
    cc = models.CharField(max_length=100, blank=False, null=False)
    comentario = models.CharField(max_length=100, blank=False, null=False)
    is_active_centro_costo = models.CharField(max_length=10, blank=False, null=False, choices=IS_ACTIVE_CHOICES,
                                              default=is_active)
    unidad_negocio = models.ForeignKey(Unidad_Negocio, on_delete=models.CASCADE)

    def __str__(self):
        return '(' + str(self.crr) + ')' + " " + self.nombre_centro_costo

    class Meta:
        verbose_name = "Centro de Costo"
        verbose_name_plural = "Centros de Costos"


# MODELO:BODEGA
class Bodega(models.Model):
    # id_bodega = models.AutoField(primary_key=True)
    nombre_bodega = models.CharField(max_length=100, blank=False, null=False)
    is_active_bodega = models.CharField(max_length=10, blank=False, null=False, choices=IS_ACTIVE_CHOICES,
                                        default=is_active)

    def __str__(self):
        return self.nombre_bodega

    class Meta:
        verbose_name = "Bodega"
        verbose_name_plural = "Bodegas"


# MODELO:CATEGORIA
class Categoria(models.Model):
    # id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=100, blank=False, null=False)
    is_active_categoria = models.CharField(max_length=10, blank=False, null=False, choices=IS_ACTIVE_CHOICES,
                                           default=is_active)

    def __str__(self):
        return self.nombre_categoria

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


# MODELO:RECURSO
unidad_1 = 'Unidad 1'
unidad_2 = 'Unidad 2'
unidad_3 = 'Unidad 3'

UNIDADES_CHOICES = [(unidad_1, 'Unidad 1'),
                    (unidad_2, 'Unidad 2'),
                    (unidad_3, 'Unidad 3'), ]


class Recurso(models.Model):
    # id_recurso = models.AutoField(primary_key=True)
    categoria_recurso = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre_recurso = models.CharField(max_length=100, blank=False, null=False)
    unidad = models.CharField(max_length=10, blank=False, null=False, choices=UNIDADES_CHOICES, default=unidad_1)
    is_active_recurso = models.CharField(max_length=10, blank=False, null=False, choices=IS_ACTIVE_CHOICES,
                                         default=is_active)

    def __str__(self):
        return self.nombre_recurso

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = "Recurso"
        verbose_name_plural = "Recursos"


# MODELO: SOLICITUD
estado_1 = 'Pendiente'
estado_2 = 'Entregado'
estado_3 = 'Rechazado'
estado_4 = 'Listo para entrega'

ESTADOS_CHOICES = [(estado_1, 'Pendiente'),
                   (estado_2, 'Entregado'),
                   (estado_3, 'Rechazado'),
                   (estado_4, 'Listo para entrega'), ]


class Observacion(models.Model):
    id_observacion = models.AutoField(primary_key=True)
    observacion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.id_observacion) + " " + str(self.observacion)

    def toJSON(self):
        item = model_to_dict(self)
        return item

class Personal(models.Model):
    id_persona = models.CharField(primary_key=True, max_length=12)
    nombre1_personal = models.CharField(max_length=50, blank=True, null=True)
    nombre2_personal = models.CharField(max_length=50, blank=True, null=True)
    apellido_p_personal = models.CharField(max_length=50, blank=True, null=True)
    apellido_m_personal = models.CharField(max_length=50, blank=True, null=True)
    is_active_personal = models.CharField(max_length=10, blank=True, null=True, choices=IS_ACTIVE_CHOICES,
                                          default=is_active)

    def __str__(self):
        return str(self.nombre1_personal) + " " + str(self.apellido_p_personal)

    def toJSON(self):
        item = model_to_dict(self)
        return item


class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_solicitud = models.DateField(blank=True, null=True)
    hora_solicitud = models.TimeField(blank=True, null=True)
    unidad_negocio = models.ForeignKey(Unidad_Negocio, on_delete=models.CASCADE)
    id_centro_costo = models.ForeignKey(Centro_Costo, on_delete=models.CASCADE)
    # edificio = models.IntegerField()
    piso = models.IntegerField()
    preparador = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="Preparador")
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, blank=True, null=True)
    estado_solicitud = models.CharField(max_length=50, blank=True, null=True, choices=ESTADOS_CHOICES, default=estado_1)
    observacion = models.ForeignKey(Observacion, on_delete=models.CASCADE)
    is_active_solicitud = models.CharField(max_length=10, blank=True, null=True, choices=IS_ACTIVE_CHOICES,
                                           default=is_active)

    def __str__(self):
        return str(self.solicitante.username)

    def toJSON(self):
        item = model_to_dict(self)
        item['solicitante'] = self.solicitante.toJSON()
        item['fecha_solicitud'] = self.fecha_solicitud.strftime('%Y-%m-%d')
        item['unidad_negocio'] = self.unidad_negocio.toJSON()
        item['id_centro_costo'] = self.id_centro_costo.toJSON()
        item['piso'] = self.piso.toJSON()
        item['preparador'] = self.preparador.toJSON()
        item['bodega'] = self.bodega.toJSON()
        item['estado_solicitud'] = self.estado_solicitud.toJSON()
        item['observacion'] = self.observacion.toJSON()
        item['is_active_solicitud'] = self.is_active_solicitud.toJSON()
        return item

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"


# MODELO: SOLICITUD_RECURSO
despacho_1 = 'No realizado'
despacho_2 = 'Realizado'

DESPACHO_CHOICES = [(despacho_1, 'No realizado'),
                    (despacho_2, 'Realizado'), ]


class Solicitud_Recurso(models.Model):
    id_solicitud_recurso = models.AutoField(primary_key=True)
    id_solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    id_recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    cantidad_solicitada = models.IntegerField()
    estado_despacho = models.CharField(max_length=15, blank=False, null=False, choices=DESPACHO_CHOICES,
                                       default=despacho_1)

    def __str__(self):
        return str(self.id_recurso.nombre_recurso)

    class Meta:
        verbose_name = "Solicitud de Recurso"
        verbose_name_plural = "Solicitudes de Recursos"
