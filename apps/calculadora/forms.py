from django import forms
from .models import *


class RestauranteForm(forms.ModelForm):
    pais = forms.ChoiceField()
    pais_input = forms.CharField(
        label='Filtrar Países',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'col-lg-6 col-md-6',
                'placeholder':'Buscar...',
                'id':'pais_input',
            }
        ),
        help_text='Seleccione su continente'
    )
    ciudad_input = forms.CharField(
        label='Filtrar Ciudades',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'col-lg-6 col-md-6',
                'placeholder':'Buscar...',
                'id':'ciudad_input',
            }
        ),
        help_text='Seleccione su continente'
    )

    class Meta:
        model = Restaurante
        fields = [
            'pais_input',
            'pais',
            'ciudad_input',
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
        self.fields['pais'] = forms.ModelChoiceField(
            queryset=Pais.objects.none(),
            widget=forms.Select(
                attrs={
                    'onchange': 'getData("id_pais", "id_ciudad")',
                    'disabled': 'true',
                    'class':'col-lg-6 col-md-6'
                }
            ),
            help_text='Seleccione su país'
        )
        self.fields['ciudad'] = forms.ModelChoiceField(
            queryset=Ciudad.objects.none(),
            widget=forms.Select(
                attrs={
                    'disabled':'true',
                    'class':'col-lg-6 col-md-6'
                }
            ),
            help_text='Seleccione su ciudad'
        )
