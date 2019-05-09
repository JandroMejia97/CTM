from django.urls import path

from . import views

app_name = 'calculadora'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('ajax/id_pais/', views.load_data, name='countries'),
    path('ajax/id_ciudad/', views.load_data, name='cities'),
    path('restaurantes/', views.RestaurantesListView.as_view(), name='restaurantes'),
    path('restaurantes/agregar/', views.RestauranteCreateView.as_view(), name='nuevo_restaurante'),

]