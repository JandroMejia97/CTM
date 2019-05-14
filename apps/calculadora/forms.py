from django import forms
from django.forms import formset_factory

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

class TipoCartaForm(forms.ModelForm):

    class Meta:
        model = TipoCarta
        fields = [
            'nombre',
            'descripcion',
            'tipo_principal',
        ]

class CartaForm(forms.ModelForm):

    class Meta:
        model = Carta
        fields = [
            'tipo'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo'] = forms.ModelChoiceField(
            queryset=Carta.objects.all(),
            help_text='Seleccione el tipo de cartas que posee su restaurante'
        )

class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        exclude = [
            'imagen',
            'descripcion',
            'carta'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update(
            {
                'placeholder': self.fields['nombre'].label,
                'title': self.fields['nombre'].help_text
            }
        )
        self.fields['precio_fijo'].widget.attrs.update(
            {
                'placeholder': self.fields['precio_fijo'].label,
                'title': self.fields['precio_fijo'].help_text,
                'min': '0.01',
            }
        )

#ProductoFormSet = formset_factory(ProductoForm, extra=2)
CartaFormSet = formset_factory(CartaForm, extra=1)