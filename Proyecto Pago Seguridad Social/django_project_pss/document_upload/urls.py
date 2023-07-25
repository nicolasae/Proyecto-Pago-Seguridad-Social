from django.urls import path
from . import views

urlpatterns = [
    path('subir_entidades/', views.upload_data_entidades, name='subir_entidades'),
    path('subir/', views.upload_documents, name='subir'),
]