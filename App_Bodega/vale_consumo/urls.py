from django.urls import path
from .views import CrearSolicitud, ListarSolicitud, ListarDetalleSolicitud
from django.contrib.auth.decorators import login_required
from vale_consumo import views


urlpatterns = [
    # Compra
    path('crear_solicitud/', login_required(CrearSolicitud.as_view()), name = 'crear_solicitud'),
    path('listar_solicitud/', login_required(ListarSolicitud.as_view()), name = 'listar_solicitud'),
    #path('listar_detalle_solicitud/', views.get_detalle_solicitudes, name='listar_detalle_solicitud'),
    path('listar_detalle_solicitud/<int:pk>', login_required(ListarDetalleSolicitud.as_view()), name='listar_detalle_solicitud'),
    #path('listar_detalle_solicitud/<int:pk>', login_required(ListarDetalleSolicitud.as_view()), name='listar_detalle_solicitud'),

]