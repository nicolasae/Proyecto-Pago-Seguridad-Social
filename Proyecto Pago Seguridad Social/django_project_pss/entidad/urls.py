from django.urls import path
from . import views

urlpatterns = [
    path('lista_gastos/', views.lista_gastos, name='lista_gastos'),
    path('cargar_datos_entidades/', views.cargar_datos_entidades, name='cargar_datos_entidades'),
]