from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', render_home_page, name = 'pagina_inicio'),
    path('admin/', admin.site.urls),
    path('documentos/', include('document_upload.urls')),
    path('informes/', include('report_generation.urls')),
]
