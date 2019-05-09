from django import forms
from .models import *


class RestauranteForm(forms.ModelForm):
    continente = forms.ChoiceField()
    pais = forms.ChoiceField()

    class Meta:
        model = Restaurante
        fields = [
            'continente',
            'pais',
            'ciudad',
            'nombre',
            'logo',
            'telefono',
            'direccion',
            'latitud',
            'longitud'
        ]
        """fieldsets = (
            ('Información General', {
                'fields': ('nombre', 'logo', 'telefono')
            }),
            ('Ubicación',{
                'fields': ('continente', 'pais', 'ciudad', 'direccion', 'latitud', 'longitud')
            })
        )"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['continente'] = forms.ModelChoiceField(
            queryset=Continente.objects.all(),
            widget=forms.Select(
                attrs={
                    'onchange':'getData("id_continente", "id_pais")',
                }
            ),
            help_text='Seleccione su continente'
        )
        self.fields['pais'] = forms.ModelChoiceField(
            queryset=Pais.objects.none(),
            widget=forms.Select(
                attrs={
                    'onchange': 'getData("id_pais", "id_ciudad")',
                    'disabled': 'true'
                }
            ),
            help_text='Seleccione su país'
        )
        self.fields['ciudad'] = forms.ModelChoiceField(
            queryset=Ciudad.objects.none(),
            widget=forms.Select(
                attrs={
                    'disabled':'true'
                }
            ),
            help_text='Seleccione su ciudad'
        )
