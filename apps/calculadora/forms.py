from django import forms
from .models import *


class RestauranteForm(forms.ModelForm):
    form_name = 'restaurante_form'

    class Meta:
        model = Restaurante
        fields = [
            'ciudad',
            'nombre',
            'logo',
        ]
