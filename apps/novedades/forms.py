from django import forms
from .forms import *


class ConsultaForm(forms.Form):
    apellidos = forms.CharField(
        max_length=100,
        required=True,
        help_text='Ingrese sus apellidos',
    )
    nombre = forms.CharField(
        max_length=100,
        required=True,
        help_text='Ingrese su nombre',
    )
    email = forms.EmailField(
        required=True,
        help_text='Ingrese su correo electrónico'
    )
    tema = forms.Select(
        max_length=50,
        required=True,
        help_text='Seleccion un tema para su consulta'
    )
    mensaje = forms.TextField(
        max_length=500,
        blank=False,
        null=False,
        help_text='Ingrese su mensaje, no olvide detalles relevantes'
    )

    class Meta:
        model = Consulta
        fields = [
            'tema', 
            'mensaje'
        ]
