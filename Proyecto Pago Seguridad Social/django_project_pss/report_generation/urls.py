from django.urls import path
from . import views

urlpatterns = [
        path('descargar/', views.download_view, name='descargar'),
]