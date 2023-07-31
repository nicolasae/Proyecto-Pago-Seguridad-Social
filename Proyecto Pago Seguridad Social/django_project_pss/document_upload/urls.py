from django.urls import path
from .views import main

urlpatterns = [
    path('subir/', main.upload_documents, name='subir'),
    path('subir/entidades/', main.upload_data_entidades, name='subir_entidades'),
    path('listar/entidades/', main.render_list_entidades, name='listar_entidades'),
    path('listar/plantillas/', main.render_list_plantillas, name='listar_plantilas'),
]