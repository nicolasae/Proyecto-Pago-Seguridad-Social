from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import *


urlpatterns = [
    path('', render_home_page, name = 'pagina_inicio'),
    path('admin/', admin.site.urls),
    path('documentos/', render_documents_page, name = 'documentos'),
    path('documentos/', include('document_upload.urls')),
    path('documentos/', include('report_generation.urls')),
]


# Configuración para servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)