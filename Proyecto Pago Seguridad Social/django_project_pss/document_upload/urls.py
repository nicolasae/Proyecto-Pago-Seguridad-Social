from django.urls import path
from . import views

urlpatterns = [
    path('cargar_datos_entidades/', views.load_data_entidades, name='cargar_datos_entidades'),
]