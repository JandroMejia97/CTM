from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'first_name',
        'last_name',
        'email',
        'fecha_nacimiento'
    ]
    fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'fecha_nacimiento'
    ]

admin.site.register(User, UserAdmin)


class IdiomaOficialAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'iso_639_1'
    ]
    fields = [
        'nombre',
        'iso_639_1'
    ]

admin.site.register(IdiomaOficial, IdiomaOficialAdmin)


class MonedaOficialAdmin(admin.ModelAdmin):
    list_display = [
        'nombre_divisa',
        'iso_4217',
        'iso_4217_numerico',
        'simbolo',
        'decimales'
    ]
    fields = [
        'nombre_divisa',
        'iso_4217',
        'iso_4217_numerico',
        'simbolo',
        'decimales'
    ]

admin.site.register(MonedaOficial, MonedaOficialAdmin)


class CiudadAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'pais',
    ]
    fields = [
        'nombre',
        'pais',
    ]

admin.site.register(Ciudad, CiudadAdmin)

class DivisionAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'ciudad',
        'latitud',
        'longitud'
    ]
    fields = [
        'nombre',
        'ciudad',
        'latitud',
        'longitud'
    ]

admin.site.register(Division, DivisionAdmin)


class ContinenteAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'codigo'
    ]
    fields = [
        'nombre',
        'codigo'
    ]

admin.site.register(Continente, ContinenteAdmin)


class PaisAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'continente',
        'iso_3166_1_2',
        'iso_3166_1_3',
        'capital',
        'moneda',
        'idioma'
    ]
    fields = [
        'nombre',
        'continente',
        'iso_3166_1_2',
        'iso_3166_1_3',
        'capital',
        'moneda',
        'idioma'
    ]

admin.site.register(Pais, PaisAdmin)


class RestauranteAdmin(admin.ModelAdmin):
    list_display = [ 
        'nombre',
        'administrador',
        'telefono',
        'barrio',
        'latitud',
        'longitud',
    ]
    fields = [ 
        'nombre',
        'logo',
        'administrador',
        'telefono',
        'barrio',
        'latitud',
        'longitud',
        'direccion',
        'mapa'
    ]

admin.site.register(Restaurante, RestauranteAdmin)


class TipoCartaAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'descripcion',
        'tipo_principal'
    ]
    fields = [
        'nombre',
        'descripcion',
        'tipo_principal'
    ]

admin.site.register(TipoCarta, TipoCartaAdmin)


class CartaAdmin(admin.ModelAdmin):
    list_display = [
        'tipo',
        'restaurante'
    ]
    fields = [
        'tipo',
        'restaurante'
    ]

admin.site.register(Carta, CartaAdmin)


class ProductoAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'precio_fijo',
        'carta'
    ]
    fields = [
        'carta',
        'nombre',
        'descripcion',
        'imagen',
        'precio_fijo'
    ]

admin.site.register(Producto, ProductoAdmin)


class PrecioAdmin(admin.ModelAdmin):
    list_display = [
        'producto',
        'monto',
        'fecha_adicion',
        'aprobaciones',
        'desaprobaciones',
    ]
    fields = [
        'producto',
        'monto',
        'moneda',
        'usuario'
    ]

admin.site.register(Precio, PrecioAdmin)


class CompraAdmin(admin.ModelAdmin):
    list_display = [
        'vendedor',
        'fecha',
        'total',
        'comprador'
    ]
    fields = [
        'vendedor',
        'fecha',
        'total',
        'comprador'
    ]

admin.site.register(Compra, CompraAdmin)


class DetalleAdmin(admin.ModelAdmin):
    list_display = [
        'compra',
        'producto',
        'unidades',
        'sub_total'
    ]
    fields = [
        'compra',
        'producto',
        'unidades',
        'sub_total'
    ]

admin.site.register(Detalle, DetalleAdmin)


class RedSocialAdmin(admin.ModelAdmin):
    list_display = [
        'nombre',
        'url'
    ]
    fields = [
        'nombre',
        'url'
    ]

admin.site.register(RedSocial, RedSocialAdmin)


class PerfilAdmin(admin.ModelAdmin):
    list_display = [
        'red_social',
        'propietario',
        'restaurante',
        'usuario'
    ]
    fields = [
        'red_social',
        'usuario',
        'url_perfil',
        'propietario',
        'restaurante'
    ]

admin.site.register(Perfil, PerfilAdmin)


class AprobacionAdmin(admin.ModelAdmin):
    list_display = [
        'usuario',
        'aprobado',
        'precio'
    ]
    fields = [
        'usuario',
        'aprobado',
        'precio'
    ]

admin.site.register(Aprobacion, AprobacionAdmin)
