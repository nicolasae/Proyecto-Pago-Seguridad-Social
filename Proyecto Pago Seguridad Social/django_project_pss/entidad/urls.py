from django.urls import path
from . import views

urlpatterns = [
    path('lista_entidades/',views.list_entidad, name='lista_entidades'),
    path('cargar_datos_entidades/', views.load_data_entidades, name='cargar_datos_entidades'),
]