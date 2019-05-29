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
        exclude = [
            '__all__'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'placeholder': self.fields[field].label,
                'title': self.fields[field].help_text,
                'class': 'form-control',
                'required': 'required'
            })
        self.fields['tipo'] = forms.ModelChoiceField(
            queryset=TipoCarta.objects.all(),
            help_text='Seleccione un tipo de carta que posee este restaurante',
            required=True
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
                'class': 'form-control',
                'required': 'required'
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

ProductoFormset = inlineformset_factory(
    parent_model=Carta,
    model=Producto,
    form=ProductoForm,
    fields=('nombre', 'precio_fijo',),
    min_num=1,
    extra=1,
    can_delete=False
)

class BaseCartaFormset(BaseInlineFormSet):

    def add_fields(self, form, index):
        super(BaseCartaFormset, self).add_fields(form, index)
        form.nested = ProductoFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='producto-%s-%s'% (
                form.prefix,
                ProductoFormset.get_default_prefix()
            )
        )

    def clean(self):
        super(BaseCartaFormset, self).clean()
        if any(self.errors):
            return
        for carta_form in self.forms:
            if carta_form.cleaned_data['tipo'] is None:
                raise forms.ValidationError('Debe añadir al menos una carta su restaurante')
            for nested_form in carta_form.nested:
                if not nested_form.is_valid():
                    raise forms.ValidationError('Debe ingresar el nombre de cada producto')
            

CartaFormset = inlineformset_factory(
    parent_model=Restaurante,
    model=Carta,
    form=CartaForm,
    fields=('tipo',),
    formset=BaseCartaFormset,
    extra=0,
    min_num=1,
    can_delete=False
)