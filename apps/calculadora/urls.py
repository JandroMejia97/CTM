from django.urls import path

from . import views

app_name = 'calculadora'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('ajax/paises/', views.get_paises, name='paises'),
    path('ajax/ciudades/', views.get_ciudades, name='ciudades'),
    path('restaurantes/', views.RestaurantesListView.as_view(), name='restaurantes'),
    path('restaurantes/agregar/', views.RestauranteCreateView.as_view(), name='nuevo_restaurante'),
    path('restaurantes/detalle/<int:pk>/', views.RestauranteUpdateView.as_view(), name='detalle_restaurante'),
]