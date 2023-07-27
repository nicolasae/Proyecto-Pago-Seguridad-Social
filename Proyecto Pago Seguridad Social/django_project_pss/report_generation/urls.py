from django.urls import path
from . import views

urlpatterns = [
        path('planilla/', views.planilla_report_view, name='planilla'),
        path('planilla/descargar/', views.create_report, name='create_report'),

]