from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import render, reverse, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.http.response import JsonResponse
from django.template.loader import render_to_string

from .forms import *
from .models import *


class RestaurantesListView(ListView, LoginRequiredMixin):
    model = Restaurante
    context_object_name = 'restaurantes'
    template_name = 'calculadora/restaurantes.html'

    def get_queryset(self):
        return Restaurante.objects.filter(administrador=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(RestaurantesListView, self).get_context_data(**kwargs)
        context['cant_restaurantes'] = context['restaurantes'].count()
        context['cant_cartas'] = 0
        context['cant_productos'] = 0
        for restaurante in context['restaurantes']:
            cartas = Carta.objects.filter(restaurante=restaurante)
            context['cant_cartas'] += cartas.count()
            for carta in cartas:
                context['cant_productos'] += Producto.objects.filter(carta=carta).count()
        return context


class RestauranteCreateView(CreateView, LoginRequiredMixin):
    model = Restaurante
    template_name = 'calculadora/restaurante.html'
    form_class = RestauranteForm
    success_url = reverse_lazy('calculadora:restaurantes')

    
    def get_context_data(self, **kwargs):
        context = super(RestauranteCreateView, self).get_context_data(**kwargs)
        context['ciudades'] = Ciudad.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        super(RestauranteCreateView, self).get(self, request, *args, **kwargs)
        context = self.get_context_data(**kwargs)
        context['carta_formset'] = CartaFormSet(request.GET or None, prefix='carta')
        context['producto_formset'] = ProductoFormSet(request.GET or None, prefix='producto')
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        restaurante_form = self.get_form(form_class)
        carta_formset = CartaFormSet(request.POST, prefix='carta')
        producto_formset = ProductoFormSet(request.POST, prefix='producto')
        if restaurante_form.is_valid() and carta_formset.is_valid() and producto_formset.is_valid():
            restaurante = Restaurante.objects.update_or_create(
                nombre=restaurante_form['nombre'].value(),
                direccion=restaurante_form['direccion'].value(),
                telefono=restaurante_form['telefono'].value(),
                mapa=restaurante_form['mapa'].value(),
                administrador=request.user,
                barrio=restaurante_form['localidad'].value()
            )
            for carta_form in carta_formset:
                carta = Carta.objects.update_or_create(
                    tipo=carta_form['tipo'],
                    restaurante=int(restaurante)
                )
                carta.save()
                for producto_form in producto_formset:
                    producto = Producto.objects.update_or_create(
                        carta=carta,
                        nombre=producto_form['nombre'],
                        precio_fijo=producto_form['precio_fijo']
                    )
                    producto.save()
            context = {
                'messages': ['El restaurante ha sido registrado exitosamente.']
            }
            return HttpResponseRedirect(self.success_url, context=context)
        else:
            context = {
                'form': restaurante_form,
                'carta_formset': carta_formset,
                'producto_formset': producto_formset,
            }
        return self.render_to_response(context)

    def form_valid(self, form, carta_formset, producto_formset):
        self.object = form.save()
        self.object.administrador = self.request.user
        carta_formset.instance = self.object
        carta_formset.save()
        producto_formset.instance = self.object
        producto_formset.save()
        context = {
            'message': 'El restaurante ha sido registrado exitosamente.'
        }
        return HttpResponseRedirect(self.success_url, context=context)
    
    def form_invalid(self, form, carta_formset, producto_formset):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                carta_formset=carta_formset,
                producto_formset=producto_formset
            )
        )


class RestauranteUpdateView(TemplateView):
    template_name = 'calculadora/restaurante_update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurante'] = Restaurante.objects.get(
            pk=self.kwargs['pk'],
            administrador=self.request.user
        )
        context['cartas'] = Carta.objects.filter(restaurante=context['restaurante'])
        for carta in context['cartas']:
            context['productos'].append(
                Producto.objects.filter(carta=carta)
            )
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['restaurante_form'] = RestauranteForm(instance=context['restaurante'])
        context['producto_formset'] = ProductoForm(instance=context['producto'])
        context['tipo_carta'] = TipoCartaForm
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        restaurante_form = RestauranteForm(data=request.POST)
        if restaurante_form.is_valid():
            restaurante = Restaurante(
                nombre=restaurante_form['nombre'].value(),
                direccion=restaurante_form['direccion'].value(),
                telefono=restaurante_form['telefono'].value(),
                administrador=request.user
            )
        else:
            context = {'errors': restaurante_form.errors}
        return self.render_to_response(context)
        

def home(request):
    return render(request, 'general/home.html', {'nav_active': 'home'})

def about(request):
    return render(request, 'general/about.html', {'nav_active': 'about'})

def load_countries(request):
    continente = request.GET['continente']
    paises = Pais.objects.filter(continente=continente)
    if paises:
        data = {
            'message': 'Datos recuperados',
            'cuentas': list(paises)
		}
    else:
        data = {
			'message': 'Aún no se registran países para el continete seleccionado'
		}
    return JsonResponse(data=data)

def get_producto_form(request):
    if request.is_ajax():
        cantidad = int(request.GET['cantidad'])
        ProductoFormSet = formset_factory(ProductoForm, extra=cantidad)
        context = {
            'producto_formset': ProductoFormSet(),
            'cant_producto_formset': cantidad,
        }
        html = render_to_string('calculadora/restaurante_producto_add.html', context=context)
        return HttpResponse(html)

def get_paises(request):
    if request.method == 'GET':
        sendData = request.GET['id']
        c = Continente.objects.get(pk=sendData)
        paises = Pais.objects.filter(continente=c).values()
        if paises:
            data = {
                'message': {
                    'user':{
                        'first_name':request.user.first_name,
                        'last_name':request.user.last_name,
                        'username':request.user.username
                    },
                    'result': 'Países recuperados exitosamente del continente ' +str(c),
                    'hora': timezone.now().strftime('%d/%m/%Y %H:%M'),
                    'alert':'check',
                    'paises': True,
                },
                'response': list(paises),
            }
        else:
            data = {
                'message': {
                    'user':{
                        'first_name':request.user.first_name,
                        'last_name':request.user.last_name,
                        'username':request.user.username
                    },
                    'result': 'Aún no se registran países para el continete '+str(c),
                    'hora': timezone.now().strftime('%d/%m/%Y %H:%M'),
                    'alert':'exclamation'
                }
            }
        return JsonResponse(data=data)

def get_ciudades(request):
    if request.method == 'GET':
        sendData = request.GET['id']
        p = Pais.objects.get(pk=sendData)
        ciudades = Ciudad.objects.filter(pais=p).values()
        if ciudades:
            data = {
                'message': {
                    'user':{
                        'first_name':request.user.first_name,
                        'last_name':request.user.last_name,
                        'username':request.user.username
                    },
                    'result': 'Ciudades recuperados exitosamente del país '+str(p),
                    'hora': timezone.now().strftime('%d/%m/%Y %H:%M'),
                    'alert':'check'
                },
                'response': list(ciudades)
            }
        else:
            data = {
                'message': {
                    'user':{
                        'first_name':request.user.first_name,
                        'last_name':request.user.last_name,
                        'username':request.user.username
                    },
                    'result': 'Aún no se registran ciudades para el país '+str(p),
                    'hora': timezone.now().strftime('%d/%m/%Y %H:%M'),
                    'alert':'exclamation'
                }
            }
        return JsonResponse(data=data)

@login_required(login_url='/sign-in/')
def get_localidades(request):
    if request.method == 'GET':
        sendData = request.GET['id']
        c = Ciudad.objects.get(pk=int(sendData))
        localidades = Division.objects.filter(ciudad=c).values()
        if localidades:
            data = {
                'message': {
                    'user':{
                        'first_name':request.user.first_name,
                        'last_name':request.user.last_name,
                        'username':request.user.username
                    },
                    'result': 'Localidades recuperadas exitosamente de la ciudad '+str(c),
                    'hora': timezone.now().strftime('%d/%m/%Y %H:%M'),
                    'alert':'check'
                },
                'response': list(localidades)
            }
        else:
            data = {
                'message': {
                    'user':{
                        'first_name':request.user.first_name,
                        'last_name':request.user.last_name,
                        'username':request.user.username
                    },
                    'result': 'Aún no se registran localidades para la ciudad '+str(c),
                    'hora': timezone.now().strftime('%d/%m/%Y %H:%M'),
                    'alert':'exclamation'
                }
            }
        return JsonResponse(data=data)

