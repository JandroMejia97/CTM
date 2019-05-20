from django.urls import path

from . import views

app_name = 'calculadora'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('ajax/paises/', views.get_paises, name='paises'),
    path('ajax/localidades/', views.get_localidades, name='localidades'),
    path('ajax/formset/producto/', views.get_producto_form, name='formset_producto'),
    path('restaurantes/', views.RestaurantesListView.as_view(), name='restaurantes'),
    path('restaurantes/agregar/', views.RestauranteCreateView.as_view(), name='nuevo_restaurante'),
    path('restaurantes/detalle/<int:pk>/', views.RestauranteUpdateView.as_view(), name='detalle_restaurante'),
]