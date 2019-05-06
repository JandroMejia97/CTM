from django import forms
from .models import *


class ConsultaForm(forms.ModelForm):
    form_name = 'consulta_form'    
    
    class Meta:
        model = Consulta
        fields = [
            'tema', 
            'mensaje'
        ]

    def __init__(self, *args, **kwargs):
        super(ConsultaForm, self).__init__(*args, **kwargs)
        self.fields['tema'] = forms.ModelChoiceField(
            queryset=Motivo.objects.all(),
            help_text='Seleccion un tema relacionado a su consulta',
        )


class ContactoForm(forms.ModelForm):
    form_name = 'contacto_form'

    class Meta:
        model = Contacto
        fields = [
            'nombre',
            'apellidos',
            'email'
        ]
