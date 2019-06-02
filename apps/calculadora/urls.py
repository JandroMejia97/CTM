from django.urls import path

from . import views

app_name = 'calculadora'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('ajax/paises/', views.get_paises, name='paises'),
    path('ajax/localidades/', views.get_localidades, name='localidades'),
    path('ajax/formset/producto/', views.get_producto_form, name='formset-producto'),
    path('ciudades/<int:pk>/restaurantes/', views.RestaurantesListView.as_view(), name='ciudades-restaurantes'),
    path('restaurantes/', views.RestaurantesListView.as_view(), name='restaurantes'),
    path('restaurantes/agregar/', views.RestauranteCreateView.as_view(), name='nuevo-restaurante'),
    path('restaurantes/detalle/<int:pk>/', views.RestauranteDetailView.as_view(), name='detalle-restaurante'),
    path('restaurantes/editar/<int:pk>/', views.RestauranteUpdateView.as_view(), name='editar-restaurante'),
    path('restaurantes/detalle/carta/agregar/', views.CartaUpdateView.as_view(), name='nueva-carta'),
    path('restaurantes/detalle/carta/detalle/<int:pk>/', views.CartaUpdateView.as_view(), {'detalle': True}, name='detalle-carta'),
    path('restaurantes/detalle/carta/editar/<int:pk>', views.CartaUpdateView.as_view(), {'detalle': False}, name='editar-carta'),
    path('restaurantes/detalle/producto/detalle/<int:pk>/', views.ProductoUpdateView.as_view(), {'detalle': True}, name='detalle-producto'),
    path('restaurantes/detalle/producto/editar/<int:pk>/', views.ProductoUpdateView.as_view(), {'detalle': False}, name='editar-producto'),
]