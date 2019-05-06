from django.shortcuts import render, render_to_response
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse

from .forms import *

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
        
            

