from django import forms
from django.forms import modelformset_factory, inlineformset_factory, BaseInlineFormSet
from django.forms.formsets import BaseFormSet

from .models import *


class RestauranteForm(forms.ModelForm):
    ciudad = forms.ChoiceField(
        error_messages={'required': 'Por favor, seleccione la ciudad donde se ubica su restaurante.'}
    )
    localidad = forms.ChoiceField(
        error_messages={'required': 'Por favor, seleccione la localidad donde se ubica su restaurante.'}
    )

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
            'localidad',
            'background'
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
        self.fields['background'].widget.attrs.update({
            'placeholder': self.fields[field].label,
            'title': self.fields[field].help_text,
            'class': ''
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
        if 'ciudad' in self.data:
            try:
                ciudad = int(self.data.get('ciudad'))
                self.fields['localidad'].queryset = Division.objects.filter(ciudad=ciudad)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['localidad'].queryset = self.instance.ciudad.localidad_set.order_by('nombre')
    

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
            })
        

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
            })
        
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

CartaFormSet = modelformset_factory(
    model=Carta,
    form=CartaForm,
    min_num=1,
    max_num=5,
    extra=2,
)
CartaInlineFormSet = inlineformset_factory(
    parent_model=Restaurante,
    model=Carta,
    extra=1,
    fields=('tipo',),
    formset=CartaFormSet,
    can_delete=False,
    min_num=1,
)
ProductoFormSet = modelformset_factory(
    model=Producto,
    form=ProductoForm,
    formset=BaseProductoFormSet,
    min_num=1,
    max_num=20,
    extra=2,
)
ProductoInlineFormSet = inlineformset_factory(
    parent_model=Carta,
    model=Producto,
    extra=2,
    fields=('nombre', 'precio_fijo',),
    formset=ProductoFormSet,
    can_delete=False,
    min_num=1
)

class BaseCartaFormset(BaseInlineFormSet):

    def add_fields(self, form, index):
        super(BaseCartaFormset, self).add_fields(form, index)
        try:
            instance = self.get_queryset()[index]
            pk_value =  instance.pk
        except IndexError:
            instance = None
            pk_value = hash(form.prefix)
        
        form.nested = [
            
        ]
        return super()