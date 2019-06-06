import unicodedata

from django import forms
from django.contrib.auth import (
    password_validation
)
from django.forms import modelformset_factory, inlineformset_factory, BaseInlineFormSet
from django.forms.formsets import BaseFormSet
from django.utils.translation import gettext, gettext_lazy as _

from .models import *

class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))

class UserForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = [
            'username',
            'is_restaurante'
        ]
        field_classes = {'username': UsernameField}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class RestauranteForm(forms.ModelForm):

    class Meta:
        prefix = 'restaurante'
        model = Restaurante
        fields = [
            'nombre',
            'telefono',
            'direccion',
            'mapa',
            'comidas',
            'ciudad',
            'barrio',
            'background'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'placeholder': self.fields[field].label,
                'title': self.fields[field].help_text,
                'class': 'form-control'
            })
        self.fields['background'].widget.attrs.update({
            'class': ''
            })
        self.fields['ciudad'] = forms.ModelChoiceField(
            queryset=Ciudad.objects.all(),
            widget=forms.Select(
                attrs={
                    'onchange':'getLocalidades("id_ciudad", "id_barrio")',
                    'class': 'form-control'
                }
            ),
            help_text='Seleccione su ciudad'
        )
        self.fields['barrio'] = forms.ModelChoiceField(
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
                self.fields['barrio'].queryset = Division.objects.filter(ciudad=ciudad)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['ciudad'].queryset = Ciudad.objects.all()
            self.fields['ciudad'].initial = self.instance.ciudad
            self.fields['barrio'].queryset = Division.objects.filter(ciudad=self.instance.ciudad)
            self.fields['barrio'].initial = self.instance.barrio
    

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
            'tipo',
        ]
        exclude = [
            'restaurante'
        ]
        # widgets = {'restaurante': forms.HiddenInput()}

    
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
    extra=0,
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