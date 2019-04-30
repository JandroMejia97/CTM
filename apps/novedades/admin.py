from django.contrib import admin

from .models import *

class ContactoAdmin(admin.ModelAdmin):
    list_display = [
        'apellidos',
        'nombre',
        'email'
    ]
    fields = [
        'apellidos',
        'nombre',
        'email'
    ]

class MotivoAdmin(admin.ModelAdmin):
    list_display = [
        'motivo',
        'descripcion'
    ]
    fields = [
        'motivo',
        'descripcion'
    ]

class ConsultaAdmin(admin.ModelAdmin):
    list_display = [
        'usuario',
        'tema',
        'mensaje'
    ]
    fields = [
        'usuario',
        'tema',
        'mensaje'
    ]

admin.site.register(Contacto, ContactoAdmin)
admin.site.register(Motivo, MotivoAdmin)
admin.site.register(Consulta, ConsultaAdmin)