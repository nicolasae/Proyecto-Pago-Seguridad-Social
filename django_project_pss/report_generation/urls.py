from django.urls import path
from .views import main

urlpatterns = [
        path('descargar/', main.download_view, name='descargar'),
]