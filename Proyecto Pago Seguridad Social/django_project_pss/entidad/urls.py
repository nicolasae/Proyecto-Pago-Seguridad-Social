from django.urls import path
from . import views

urlpatterns = [
    path('lista_gastos/', views.lista_gastos, name='lista_gastos'),
]