from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
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

from operator import itemgetter
from itertools import groupby

from .forms import *
from .models import *


class UserCreateView(CreateView):
    model = User
    template_name = 'registration/signup.html'
    form_class = UserForm
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            if user.is_restaurante:
                grupo = Group.objects.get(name='Administrador de Restaurante')
                grupo.user_set.add(user)
            return self.get_success_url()
        else:
            context = {
                'form': form
            }
            self.render_to_response(context)


class RestaurantesListView(ListView):
    model = Restaurante
    context_object_name = 'restaurantes'
    template_name = 'calculadora/restaurantes_admin.html'

    def get_queryset(self):
        if 'pk' in self.kwargs:
            barrios =  Division.objects.filter(ciudad=self.kwargs['pk'])
            return Restaurante.objects.filter(barrio__in=barrios)
        elif self.request.user.is_authenticated:
            return Restaurante.objects.filter(administrador=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(RestaurantesListView, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            context['ciudad'] = Ciudad.objects.get(pk=self.kwargs['pk'])
            comidas = TipoComida.objects.all()
            group = {}
            for comida in comidas:
                restaurante_key = '_'.join([str(restaurante.pk) for restaurante in comida.restaurante_set.all()])
                if not restaurante_key in group and restaurante_key != '':
                    group[restaurante_key]={'restaurantes': comida.restaurante_set.all(), 'comidas':[]}
                if restaurante_key != '':
                    group[restaurante_key]['comidas'].append(comida)    
            context['group'] = group
        elif self.request.user.is_authenticated:
            cartas = Carta.objects.filter(restaurante__in=context['restaurantes'])
            productos = Producto.objects.filter(carta__in=cartas)
            context['cant_restaurantes'] = context['restaurantes'].count()
            context['cant_cartas'] = cartas.count()
            context['cant_productos'] = productos.count()
        return context

    def get_template_names(self):
        if 'pk' in self.kwargs:
            template_name = 'calculadora/restaurantes.html'
        else:
            template_name = self.template_name
        return template_name


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
                # background=restaurante_form['background'].value(),
            )
            tipos_comida = TipoComida.objects.filter(pk__in=restaurante_form['comida'].value())
            restaurante.save()
            for tipo_comida in tipos_comida:
                restaurante.comidas.add(tipo_comida)
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
                            nombre=producto_form['nombre'].value(),
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


class RestauranteDetailView(DetailView):
    model = Restaurante
    context_object_name = 'restaurante'
    template_name = 'calculadora/restaurante_detail_template.html'

    def get_context_data(self, **kwargs):
        context = super(RestauranteDetailView, self).get_context_data(**kwargs)
        context['cartas'] = Carta.objects.filter(restaurante=context['restaurante']).annotate(num_products=Count('producto'))
        context['productos'] = Producto.objects.filter(carta__in=context['cartas'])
        context['perfiles'] = Perfil.objects.filter(restaurante=context['restaurante'])
        return context


class CartaCreateView(LoginRequiredMixin, CreateView):
    model = Carta
    template_name = 'calculadora/carta_create_template.html'
    form_class = CartaForm

    def get_context_data(self, **kwargs):
        context = super(CartaCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = CartaForm(self.request.POST, instance=self.object)
            context['producto_formset'] = ProductoFormset(self.request.POST, instance=self.object)
        else:
            context['form'] = CartaForm(instance=self.object)
            context['producto_formset'] = ProductoFormset(instance=self.object)

        if 'pk' in self.kwargs:
            context['restaurante'] = Restaurante.objects.get(pk=self.kwargs['pk'])
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        producto_formset = ProductoFormset(self.request.POST)
        if form.is_valid() and producto_formset.is_valid():
            return self.form_valid(form, producto_formset)
        else:
            return self.form_invalid(form, producto_formset)
        return super(CartaCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form, producto_formset):
        carta, created = Carta.objects.update_or_create(
            tipo=TipoCarta.objects.get(pk=int(form['tipo'].value())),
            restaurante=Restaurante.objects.get(pk=self.kwargs['pk'])
        )
        carta.save()
        self.object = carta
        producto_formset.instance = carta
        producto_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, producto_formset):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                producto_formset=producto_formset
            )
        )

    def get_success_url(self):
        return reverse('calculadora:detalle-restaurante', kwargs={'pk':self.object.restaurante.pk})


class CartaUpdateView(LoginRequiredMixin, UpdateView):
    model = Carta
    template_name = 'calculadora/carta_detail_template.html'
    form_class = CartaForm

    def get_context_data(self, **kwargs):
        context = super(CartaUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            if 'detalle' in self.kwargs:
                context['detalle'] = self.kwargs['detalle']
                context['form'] = CartaForm(self.request.POST, instance=self.object)
                context['producto_formset'] = ProductoFormset(self.request.POST, instance=self.object)
        else:
            if 'detalle' in self.kwargs:
                context['detalle'] = self.kwargs['detalle']
                context['form'] = CartaForm(instance=self.object)
                context['producto_formset'] = ProductoFormset(instance=self.object)
        context['carta'] = self.object
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        producto_formset = ProductoFormset(self.request.POST)
        if form.is_valid() and producto_formset.is_valid():
            return self.form_valid(form, producto_formset)
        else:
            return self.form_invalid(form, producto_formset)
        return super(CartaUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form, producto_formset):
        carta, created = Carta.objects.get_or_create(
            tipo=TipoCarta.objects.get(pk=int(form['tipo'].value())),
            restaurante=Restaurante.objects.get(pk=int(form['restaurante'].value())),
        )
        if created:
            carta.save()
        self.object = carta
        producto_formset.instance = carta
        producto_formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, producto_formset):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                producto_formset=producto_formset
            )
        )

    def get_success_url(self):
        return reverse('calculadora:detalle-restaurante', kwargs={'pk':self.object.restaurante.pk})


class ProductoListView(ListView):
    model = Producto
    context_object_name = 'productos'
    template_name = 'calculadora/restaurante_producto_list_template.html'

    def get_queryset(self):
        cartas = Carta.objects.filter(restaurante=self.kwargs['restaurante_pk'])
        return Producto.objects.filter(carta__in=cartas)

    def get_context_data(self, **kwargs):
        context = super(ProductoListView, self).get_context_data(**kwargs)
        context['restaurante'] = Restaurante.objects.get(pk=self.kwargs['restaurante_pk'])
        context['perfiles'] = Perfil.objects.filter(restaurante=context['restaurante'])
        return context


class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    template_name = 'calculadora/producto_detail_template.html'
    fields = [
        'nombre',
        'descripcion',
        'precio_fijo'
    ]

    def get_success_url(self):
        return reverse('calculadora:detalle-restaurante', kwargs={'pk':self.object.carta.restaurante.pk})



class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    template_name = 'calculadora/producto_detail_template.html'
    fields = [
        'nombre',
        'descripcion',
        'precio_fijo'
    ]

    def get_context_data(self, **kwargs):
        context = super(ProductoUpdateView, self).get_context_data(**kwargs)
        if 'detalle' in self.kwargs:
            context['detalle'] = self.kwargs['detalle']
        context['producto'] = Producto.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('calculadora:detalle-restaurante', kwargs={'pk':self.object.carta.restaurante.pk})


class PerfilCreateView(LoginRequiredMixin, CreateView):
    model = Perfil
    template_name = 'calculadora/perfil_create_template.html'
    fields = [
        'red_social',
        'usuario',
        'url_perfil'
    ]

    def get_context_data(self, **kwargs):
        context = super(PerfilCreateView, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            context['restaurante'] = Restaurante.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        perfil, created = Perfil.objects.update_or_create(
            usuario=form['usuario'].value(),
            url_perfil=form['url_perfil'].value(),
            red_social=RedSocial.objects.get(pk=form['red_social'].value()),
            restaurante=Restaurante.objects.get(pk=self.kwargs['pk']),
            propietario=self.request.user,
        )
        perfil.save()
        self.object = perfil
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('calculadora:detalle-restaurante', kwargs={'pk':self.object.restaurante.pk})


class PerfilUpdateView(LoginRequiredMixin, UpdateView):
    model = Perfil
    template_name = 'calculadora/perfil_detail_template.html'
    fields = [
        'red_social',
        'usuario',
        'url_perfil'
    ]
    
    def get_context_data(self, **kwargs):
        context = super(PerfilUpdateView, self).get_context_data(**kwargs)
        if 'detalle' in self.kwargs:
            context['detalle'] = self.kwargs['detalle']
        context['perfil'] = self.object
        return context
    
    def get_success_url(self):
        return reverse('calculadora:detalle-perfil', kwargs={'pk':self.object.restaurante.pk})

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

def get_update_precio_form(request, pk):
    if request.method == 'POST':
        nuevo_precio = request.POST['precio']
        producto = Producto.objects.get(pk=pk)
        precio = Precio.objects.create(
            usuario=request.user,
            producto=producto,
            monto=nuevo_precio
        )
        context = {
            'messages': ['El nuevo precio fue registrado exitosamente, a la espera de ser aprobado por otros usuarios.'],
            'success': True
        }
        html = render_to_string(request=request, template_name='messages.html', context=context)
        return HttpResponse(html)
    else:
        producto = Producto.objects.get(pk=pk)
        precios = Precio.objects.filter(producto=producto)[:3]
        aprobaciones = Aprobacion.objects.filter(usuario=request.user, precio__in=precios)
        for precio in precios:
            precio.usuario_aprobo = (request.user in precio.get_usuarios_aprobaron())
            precio.usuario_desaprobo = (request.user in precio.get_usuarios_desaprobaron())
        context = {
            'precios': precios,
            'producto': producto, 
            'aprobaciones': aprobaciones
        }
        html = render_to_string(request=request, template_name='calculadora/restaurante_update_precio_template.html', context=context)
        return HttpResponse(html)

def set_aprobacion(request, pk, aprobado):
    precio = Precio.objects.get(pk=pk)
    if Aprobacion.objects.filter(usuario=request.user, precio=precio).exists():
        aprobacion = Aprobacion.objects.get(
            usuario=request.user,
            precio=precio
        )
    else:
        aprobacion = Aprobacion(
            usuario=request.user,
            precio=precio
        )
    aprobacion.aprobado = aprobado
    aprobacion.save()
    precio.aprobaciones = Aprobacion.objects.filter(precio=precio, aprobado=True).count()
    precio.aprobaciones = Aprobacion.objects.filter(precio=precio, aprobado=True).count()
    precio.save()
    messages = []
    if aprobado:
        messages.append('Su aprobación a este precio fue registrada exitosamente.')
    else: 
        messages.append('Su desaprobación a este precio fue registrada exitosamente.')
    context = {
            'messages': messages,
            'success': True
        }
    html = render_to_string(request=request, template_name='messages.html', context=context)
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

