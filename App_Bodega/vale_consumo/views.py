import json
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.http import JsonResponse
from .models import Solicitud, Recurso, Solicitud_Recurso, Centro_Costo
from .forms import SolicitudForm


# Create your views here.

# Vistas basadas en clases
class ListarSolicitud(ListView):
    model = Solicitud
    paginate_by = 10
    template_name = "vale_consumo/listar_vale.html"
    context_object_name = 'solicitudes'
    queryset = Solicitud.objects.all().order_by('-fecha_solicitud')


class CrearSolicitud(CreateView):
    model = Solicitud
    form_class = SolicitudForm
    context_object_name = 'centros'
    queryset = Centro_Costo.objects.all()
    template_name = 'vale_consumo/crear_vale.html'
    success_url = reverse_lazy('vale_consumo/listar_vale.html')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                print("Buscar productos")
                data = []
                prods = Recurso.objects.filter(nombre_recurso__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.nombre_recurso
                    data.append(item)
            elif action == 'add':
                vents = json.loads(request.POST['vents'])
                print(vents)
                soli = Solicitud()
                soli.fecha_solicitud = vents['fecha_solicitud']
                soli.solicitante_id = vents['solicitante']
                soli.unidad_negocio_id = vents['unidad_negocio']
                soli.id_centro_costo_id = vents['id_centro_costo']
                soli.piso = vents['piso']
                soli.retira = vents['retira']
                soli.save()
                print("LLEGA AL GUARDADO DE EL ENCABEZADO")
                for i in vents['recursos']:
                    sol_rec = Solicitud_Recurso()
                    sol_rec.id_solicitud_id = soli.id_solicitud
                    sol_rec.id_recurso_id = int(i['id'])
                    sol_rec.cantidad_solicitada = int(i['cantidad_solicitada'])
                    sol_rec.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = e
        return JsonResponse(data, safe=False)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Creación de una Venta'
        # context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

def get_centros_costos(request):
    unidad_negocio_id = request.GET.get('unidad_negocio_id')
    centros_costos = Centro_Costo.objects.filter(unidad_negocio_id=unidad_negocio_id).values('id','nombre_centro_costo')
    return JsonResponse(list(centros_costos), safe=False)

class ListarDetalleSolicitud(DetailView):
    model = Solicitud
    # paginate_by = 1
    template_name = 'vale_consumo/listar_detalle_Solicitud.html'
    context_object_name = 'solicitud'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solicitud = self.get_object()  # Obtiene la solicitud actual

        # Obtén los detalles de los recursos asociados a esta solicitud
        detalles_recursos = solicitud.solicitud_recurso_set.all()
        context['detalles_recursos'] = detalles_recursos

        return context
