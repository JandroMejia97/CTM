from django.urls import path

from . import views

app_name = 'novedades'

urlpatterns = [
    path('contact/', views.ConsultaCreateView.as_view(), name='contact'),
]