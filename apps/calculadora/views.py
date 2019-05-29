from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import render, render_to_response, reverse, HttpResponse, HttpResponseRedirect
from django.views.defaults import page_not_found
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.http.response import JsonResponse
from django.template.loader import render_to_string

from nested_formset import nestedformset_factory

from .forms import *
from .models import *


class RestaurantesListView(LoginRequiredMixin, ListView):
    model = Restaurante
    context_object_name = 'restaurantes'
    template_name = 'calculadora/restaurantes.html'

    def get_queryset(self):
        if('pk' in self.kwargs):
            barrios =  Division.objects.filter(ciudad=self.kwargs['pk'])
            return Restaurante.objects.filter(pk__in=barrios)
        else:
            return Restaurante.objects.filter(administrador=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(RestaurantesListView, self).get_context_data(**kwargs)
        cartas = Carta.objects.filter(restaurante__in=context['restaurantes'])
        productos = Producto.objects.filter(carta__in=cartas)
        context['cant_restaurantes'] = context['restaurantes'].count()
        context['cant_cartas'] = cartas.count()
        context['cant_productos'] = productos.count()
        return context


class RestauranteCreateView(LoginRequiredMixin, CreateView):
    model = Restaurante
    template_name = 'calculadora/restaurante.html'
    form_class = RestauranteForm
    success_url = reverse_lazy('calculadora:restaurantes')

    def get(self, request, *args, **kwargs):
        super(RestauranteCreateView, self).get(self, request, *args, **kwargs)
        context = self.get_context_data(**kwargs)
        context['carta_formset'] = CartaFormset()
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        restaurante_form = self.get_form(form_class)
        carta_formset = CartaFormset(request.POST)
        if restaurante_form.is_valid() and carta_formset.is_valid():
            restaurante = Restaurante(
                nombre=restaurante_form['nombre'].value(),
                direccion=restaurante_form['direccion'].value(),
                telefono=restaurante_form['telefono'].value(),
                mapa=restaurante_form['mapa'].value(),
                administrador=request.user,
                barrio=Division.objects.get(pk=int(request.POST['barrio'])),
                ciudad=Ciudad.objects.get(pk=int(request.POST['ciudad'])),
                background=restaurante_form['background'].value(),
            )
            tipos_comida = TipoComida.objects.filter(pk__in=restaurante_form['tipo_comida'].value())
            restaurante.save()
            for tipo_comida in tipos_comida:
                restaurante.tipo_comida.add(tipo_comida)
            for carta_form in carta_formset:
                if carta_form.is_valid():
                    tipo = int(carta_form['tipo'].value())
                    tipo_carta = TipoCarta.objects.get(pk=tipo)
                    carta = Carta(
                        tipo=tipo_carta,
                        restaurante=restaurante
                    )
                    carta.save()
                    for producto_form in carta_form.nested:
                        if producto_form.is_valid():
                            producto = Producto(
                            carta=carta,
                            nombre=producto_form['nombre'],
                            precio_fijo=float(producto_form['precio_fijo'].value())
                        )
                        producto.save()
            restaurante.save()
            context = {
                'messages': ['El restaurante ha sido registrado exitosamente.']
            }
            return HttpResponseRedirect(self.success_url)
        else:
            context = {
                'form': restaurante_form,
                'messages': [
                    'El restaurante no pudo ser registrado. Corrija los siguiente errores.',
                ],
                'carta_formset': carta_formset,
            }
        return self.render_to_response(context)


class RestauranteUpdateView(LoginRequiredMixin, UpdateView):
    model = Restaurante
    template_name = 'calculadora/restaurante.html'
    form_class = RestauranteForm
    success_url = reverse_lazy('calculadora:restaurantes')
    
    def get_context_data(self, **kwargs):
        context = super(RestauranteUpdateView, self).get_context_data(**kwargs)
        context['restaurante'] = Restaurante.objects.get(
            pk=self.kwargs['pk'],
            administrador=self.request.user
        )
        return context

    def get(self, request, *args, **kwargs):
        super(RestauranteUpdateView, self).get(self, request, *args, **kwargs)
        context = self.get_context_data(**kwargs)
        context['form'] = RestauranteForm(instance=context['restaurante'])
        carta = Carta.objects.filter(restaurante=context['restaurante'])
        context['carta_formset'] = CartaFormset(instance=context['restaurante'])
        context['update'] = True
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
    ciudades = Ciudad.objects.all()
    context ={
        'ciudades': ciudades,
        'nav_active': 'home'
    }
    return render(request, 'general/home.html', context)

def about(request):
    return render(request, 'general/about.html', {'nav_active': 'about'})

def get_403(request):
    template_name = 'errors/403.html'
    return render(request, template_name, {})

def get_404(request):
    template_name = 'errors/404.html'
    return render(request, template_name, {})

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

