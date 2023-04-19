from django.db import models
from usuario.models import UserProfile
from vale_consumo.models import Recurso
# Create your models here.

is_active = 'Activo'
is_inactive = 'Inactivo'

IS_ACTIVE_CHOICES =[(is_active, 'Activo'),
                    (is_inactive, 'Inactivo'),]

class Familia(models.Model):
    id_familia = models.AutoField(primary_key=True)
    nombre_familia = models.CharField(max_length=100, blank=False, null=False)
    #producto_hijo = models.ForeignKey(Producto, on_delete=models.CASCADE)
    is_active = models.CharField(max_length=100, blank=False, null=False)

class Inventario(models.Model):
    id_inventaro = models.AutoField(primary_key=True)
    encargado = models. ForeignKey(UserProfile, on_delete=models.CASCADE)
    fecha_inventario = models.DateField(blank=True, null=True)
    is_active_inventario = models.CharField(max_length=10, blank=False, null=False, choices=IS_ACTIVE_CHOICES, default=is_active)

class Detalle_Inventario(models.Model):
    id_detalle_inventario = models.AutoField(primary_key=True)
    no_inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    recurso_inventariado = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    cantidad_inventariada = models.IntegerField()

    def __str__(self):
        return self.id_recurso.nombre_recurso
    class Meta:
        verbose_name = "Detalle de inventario"
        verbose_name_plural = "Detalle de inventarios"