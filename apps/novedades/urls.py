from django.urls import path

from . import views

app_name = 'novedades'

urlpatterns = [
    path('contact/', views.ConsultaCreateView.as_view(), name='contact'),
    path('continentes/', views.import_continent, name='continent'),
    path('idiomas/', views.import_language, name='lang'),
    path('monedas/', views.import_currencies, name='currency'),
    path('paises/', views.import_country, name='country'),
    path('productos/', views.import_products, name='products'),
]