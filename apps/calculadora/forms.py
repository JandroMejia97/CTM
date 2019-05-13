from django import forms
from .models import *


class RestauranteForm(forms.ModelForm):

    class Meta:
        model = Restaurante
        fields = [
            'nombre',
            'telefono',
            'direccion',
            'mapa'
        ]
    