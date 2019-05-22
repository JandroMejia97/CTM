from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.forms.formsets import BaseFormSet

from .models import *


class RestauranteForm(forms.ModelForm):
    ciudad = forms.ChoiceField()
    localidad = forms.ChoiceField()

    class Meta:
        prefix = 'restaurante'
        model = Restaurante
        fields = [
            'nombre',
            'telefono',
            'direccion',
            'mapa',
            'tipo_comida',
            'ciudad',
            'localidad'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'placeholder': self.fields[field].label,
                'title': self.fields[field].help_text,
                'class': 'form-control'
                }
            )
        self.fields['ciudad'] = forms.ModelChoiceField(
            queryset=Ciudad.objects.all(),
            widget=forms.Select(
                attrs={
                    'onchange':'getLocalidades("id_ciudad", "id_localidad")',
                    'class': 'form-control'
                }
            ),
            help_text='Seleccione su ciudad'
        )
        self.fields['localidad'] = forms.ModelChoiceField(
            queryset=Division.objects.none(),
            widget=forms.Select(
                attrs={
                    'class': 'form-control',
                    'disabled': 'disabled'
                }
            ),
            help_text='Seleccione su ciudad'
        )
    

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
        prefix = 'carta'
        fields = [
            'tipo'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'placeholder': self.fields[field].label,
                'title': self.fields[field].help_text,
                'class': 'form-control'
                }
            )
        

class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        prefix = 'producto'
        fields = [
            'nombre',
            'precio_fijo'
        ]
        exclude = [
            'imagen',
            'descripcion',
            'carta'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'placeholder': self.fields[field].label,
                'title': self.fields[field].help_text,
                'class': 'form-control'
                }
            )
        
        self.fields['precio_fijo'].widget.attrs.update({'min': '0.01'})

class BaseProductoFormSet(BaseFormSet):

    def clean(self):
        
        if any(self.errors):
            return 
        
        nombres = []
        precios_fijos = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                nombre = form.cleaned_data['nombre']
                precio_fijo = form.cleaned_data['precio_fijo']

                if nombre and precio_fijo:
                    if nombre in nombres:
                        duplicates = True
                    nombres.append(nombre)
                
                if duplicates:
                    raise forms.ValidationError(
                        'El nombre de los productos ingresados deben ser distintos.',
                        code='duplicate_nombres'
                    )

                if nombre and not precio_fijo:
                    raise forms.ValidationError(
                        'Para cada producto debe ingresar su respectivo precio',
                        code='missing_precio_fijo'
                    )
                elif precio_fijo and not nombre:
                    raise forms.ValidationError(
                        'Para cada producto debe ingresar su respectivo nombre',
                        code='missing_nombre'
                    )


"""
ProductoFormSet = formset_factory(
    ProductoForm,
    formset=BaseProductoFormSet,
    min_num=1,
    max_num=20,
    extra=0
)"""

ProductoFormSet = inlineformset_factory(
    parent_model=Carta,
    model=Producto,
    form=ProductoForm,
    min_num=1,
    max_num=5,
    extra=0,
    can_delete=True
)
CartaFormSet = inlineformset_factory(
    parent_model=Restaurante,
    model=Carta,
    form=CartaForm,
    min_num=1,
    max_num=5,
    extra=0,
    can_delete=True
)