from django.urls import path
from . import views

urlpatterns = [
    path('cargar_datos_entidades/', views.cargar_datos_entidades, name='cargar_datos_entidades'),
]