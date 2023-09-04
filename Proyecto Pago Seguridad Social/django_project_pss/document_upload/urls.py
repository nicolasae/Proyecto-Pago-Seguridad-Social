from django.urls import path
from .views import main
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('subir/', login_required(main.upload_documents), name='subir'),
    path('subir/entidades/', login_required(main.upload_data_entidades), name='subir_entidades'),
    path('listar/entidades/', main.render_list_entidades, name='listar_entidades'),
    path('listar/plantillas/', main.render_list_plantillas, name='listar_plantilas'),
]