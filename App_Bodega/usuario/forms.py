from django.contrib.auth.forms import AuthenticationForm
from django import forms


class FormularioLogin(AuthenticationForm):
    def _init_(self, *args, **kwargs):
        super(FormularioLogin, self)._init_(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

