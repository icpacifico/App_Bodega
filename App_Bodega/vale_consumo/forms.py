from django.forms import *
import datetime
from .models import Solicitud
from django.contrib.auth.models import User


class SolicitudForm(ModelForm):
    class Meta:
        model = Solicitud
        fields = '__all__'
        widgets = {
            'solicitante': Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'unidad_negocio': Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_centro_costo': Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'piso': TextInput(
                attrs={
                    'class': 'form-control ',
                    'type': 'number',
                    'min': 1,
                }
            ),
            'retira': TextInput(
                attrs={
                    'class': 'form-control ',
                }
            )
        }

    fecha_solicitud = DateField(widget=NumberInput(attrs={'type': 'date', 'class': 'form-control '}),
                                initial=datetime.date.today)


