from django.urls import path

from . import views

app_name = 'novedades'

urlpatterns = [
    path('contact/', views.ConsultaCreateView.as_view(), name='contact'),
    path('continentes/', views.import_continent, name='continent'),
    path('paises/', views.import_country, name='country'),
]