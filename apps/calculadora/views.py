from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.http.response import JsonResponse

from .forms import *
from .models import *


class RestaurantesListView(ListView):
    model = Restaurante
    context_object_name = 'restaurantes'
    template_name = 'calculadora/restaurantes.html'

    def get_queryset(self):
        return Restaurante.objects.filter(administrador=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cant_restaurantes'] = context['restaurantes'].count()
        context['cant_cartas'] = 0
        context['cant_productos'] = 0
        for restaurante in context['restaurantes']:
            cartas = Carta.objects.filter(restaurante=restaurante)
            context['cant_cartas'] += cartas.count()
            for carta in cartas:
                context['cant_productos'] += Producto.objects.filter(carta=carta).count()
        return context


class RestauranteCreateView(TemplateView):
    template_name = 'calculadora/restaurante.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['continentes'] = Continente.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['restaurante_form'] = RestauranteForm
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        restaurante_form = RestauranteForm(data=request.POST)
        if restaurante_form.is_valid():
            restaurante = Restaurante(
                nombre=restaurante_form['nombre'].value(),
                logo=restaurante_form['logo'].value(),
                latitud=restaurante_form['latitud'].value(),
                longitud=restaurante_form['longitud'].value(),
                direccion=restaurante_form['direccion'].value(),
                telefono=restaurante_form['telefono'].value(),
                ciudad=restaurante_form['ciudad'].value(),
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

def load_data(request):
    if request.method == 'GET':
        sendData = request.GET['data']
        case = request.GET['case']
        if case == 'id_continente':
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
        elif case == 'id_pais':
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

