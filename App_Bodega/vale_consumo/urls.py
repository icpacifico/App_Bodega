from django.urls import path
from .views import CrearSolicitud, ListarSolicitud
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Compra
    path('crear_solicitud/', login_required(CrearSolicitud.as_view()), name = 'crear_solicitud'),
    path('listar_solicitud/', login_required(ListarSolicitud.as_view()), name = 'listar_solicitud'),

]