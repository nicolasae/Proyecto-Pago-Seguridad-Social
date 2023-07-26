from django.urls import path
from .views import main

urlpatterns = [
    path('subir_entidades/', main.upload_data_entidades, name='subir_entidades'),
    path('subir/', main.upload_documents, name='subir'),
]