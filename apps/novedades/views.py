from django.shortcuts import render, render_to_response
from django.http.response import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from django.urls import reverse

from .forms import *
from apps.calculadora.models import *

class ConsultaCreateView(TemplateView):
    template_name = 'general/contact.html'
    success_url = 'calculadora:home'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.user.is_authenticated:
            user = request.user
            context['contacto_form'] =  ContactoForm(
                initial={
                    'apellidos': user.last_name,
                    'nombre': user.first_name,
                    'email': user.email
                }
            )
        else:
            context['contacto_form'] = ContactoForm()
        context['consulta_form'] = ConsultaForm()
        context['nav_active'] = 'contact'
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        contacto_form = ContactoForm(data=request.POST)
        consulta_form = ConsultaForm(data=request.POST)
        if consulta_form.is_valid() and contacto_form.is_valid():
            contacto, encontrado = Contacto.objects.get_or_create(
                apellidos=contacto_form['apellidos'].value(),
                nombre=contacto_form['nombre'].value(),
                email=contacto_form['email'].value()
            )
            motivo = Motivo.objects.get(pk=consulta_form['tema'].value())
            consulta = Consulta(
                tema=motivo,
                mensaje=consulta_form['mensaje'].value(),
                usuario=contacto
            )
            consulta.save()
            context = {
                'messages': ['Su consulta ha sido enviada exitosamente'],
                'nav_active': 'home'
            }
            return render_to_response('general/home.html', context)

import pandas as pd  
import os      

def import_continent(request):
    url = os.getcwd()+'/data/continent.csv'
    data = pd.read_csv(url,  encoding="ISO-8859-1", engine='python')
    for row in data.itertuples(index=False):
        c = Continente.objects.update_or_create(
            nombre=row.Name,
            codigo=row.Code
        )
    return HttpResponse('Los datos de los continentes han sido importados exitosamente')

def import_language(request):
    url = os.getcwd()+'/data/idiomas.csv'
    data = pd.read_csv(url,  encoding="ISO-8859-1", engine='python')
    for row in data.itertuples(index=False):
        i = IdiomaOficial.objects.update_or_create(
            nombre=row.English,
            iso_639_1=row.alpha2
        )
    return HttpResponse('Los datos de los idiomas han sido importados exitosamente')

def import_currencies(request):
    url = os.getcwd()+'/data/divisas.csv'
    data = pd.read_csv(url,  encoding="ISO-8859-1", engine='python')
    for row in data.itertuples(index=False):
        m = MonedaOficial.objects.update_or_create(
            nombre_divisa=row.CurrencyName,
            iso_4217=row.CurrencyCode
        )
    return HttpResponse('Los datos de los divisas han sido importados exitosamente')

def import_products(request):
    url = os.getcwd()+'/data/calculadora_producto2.csv'
    data = pd.read_csv(url,  encoding="ISO-8859-1", engine='python')
    for row in data.itertuples(index=False):
        c = Carta.objects.get(pk=int(row.carta_id))
        p = Producto.objects.update_or_create(
            nombre=row.nombre,
            descripcion=row.descripcion,
            precio_fijo=row.precio_fijo,
            carta=c
        )
    return HttpResponse('Los datos de los productos han sido importados exitosamente')

def import_localidades(request):
    url = os.getcwd()+'/data/localidades.csv'
    data = pd.read_csv(url, sep=';', encoding="ISO-8859-1", engine='python')
    for row in data.itertuples(index=False):
        c = Ciudad.objects.get(nombre=row.ciudad)
        d = Division.objects.update_or_create(
            nombre=row.localidad,
            ciudad=c
        )
    return HttpResponse('Los datos de las localidades han sido importados exitosamente')

def import_cartas(request):
    url = os.getcwd()+'/data/tipocarta.csv'
    data = pd.read_csv(url, sep=';', encoding="ISO-8859-1", engine='python')
    for row in data.itertuples(index=False):
        if str(row.tipo_principal_id).upper() != 'NAN':
            tipo_principal = TipoCarta.objects.get(pk=int(row.tipo_principal_id))
            tipo = TipoCarta.objects.update_or_create(
                nombre=row.nombre,
                descripcion=row.descripcion,
                tipo_principal=tipo_principal
            )
        else:
            tipo = TipoCarta.objects.update_or_create(
                nombre=row.nombre,
                descripcion=row.descripcion
            )
    return HttpResponse('Los datos de las cartas han sido importados exitosamente')

def import_country(request):
    url = os.getcwd()+'/data/country_new.csv'
    data = pd.read_csv(url, encoding="ISO-8859-1", engine='python')
    print(data)
    columnas = [
        'ISO3166_1_numeric',
        'ISO4217_currency_numeric_code',
        'Capital',
        'Languages'
    ]
    print(data)
    data = data.drop(columns=columnas)
    for row in data.itertuples(index=False):
        print(row)
        c = Continente.objects.get(
            codigo=row.Continent
        )
        p = Pais.objects.update_or_create(
            nombre=row.official_name_es,
            iso_3166_1_2=row.ISO3166_1_Alpha_2,
            iso_3166_1_3=row.ISO3166_1_Alpha_3,
            continente=c
        )
    return HttpResponse('Los datos de los países han sido importados exitosamente')
