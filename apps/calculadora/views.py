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
        context['ciudades'] = Ciudad.objects.all()
        """context['carta_formset'] = nestedformset_factory(
            parent_model=Restaurante,
            model=Carta,
            form=CartaForm,
            min_num=1,
            max_num=5,
            extra=1,
            can_delete=False,
            nested_formset=inlineformset_factory(
                parent_model=Carta,
                model=Producto,
                form=ProductoForm,
                min_num=1,
                max_num=20,
                extra=1,
                can_delete=False,
            )
        )
        # context['carta_formset'] = CartaInlineFormSet(request.GET or None, prefix='carta', queryset=Carta.objects.all())
        # context['producto_formset'] = ProductoInlineFormSet(request.GET or None, prefix='producto')"""
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        restaurante_form = self.get_form(form_class)
        # carta_formset = CartaFormSet(request.POST, prefix='seccion')
        # producto_formset = ProductoFormSet(request.POST, prefix='producto')
        # if restaurante_form.is_valid() and carta_formset.is_valid() and producto_formset.is_valid():
        if restaurante_form.is_valid() and 'localidad' in request.POST:
            localidad = int(request.POST['localidad'])
            localidad = Division.objects.get(pk=localidad)
            restaurante = Restaurante(
                nombre=restaurante_form['nombre'].value(),
                direccion=restaurante_form['direccion'].value(),
                telefono=restaurante_form['telefono'].value(),
                mapa=restaurante_form['mapa'].value(),
                administrador=request.user,
                barrio=localidad,
                background=restaurante_form['background'].value(),
            )
            tipos_comida = TipoComida.objects.filter(pk__in=restaurante_form['tipo_comida'].value())
            restaurante.save()
            for tipo_comida in tipos_comida:
                restaurante.tipo_comida.add(tipo_comida)
            """for carta_form in carta_formset:
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
                    producto.save()"""
            restaurante.save()
            context = {
                'messages': ['El restaurante ha sido registrado exitosamente.']
            }
            return HttpResponseRedirect(self.success_url)
        else:
            context = {
                'form': restaurante_form,
                'ciudades': Ciudad.objects.all(),
                'messages': [
                    'El restaurante no pudo ser registrado. Corrija los siguiente errores.',
                ]
                # 'carta_formset': carta_formset,
                # 'producto_formset': producto_formset,
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

