import openpyxl
from django.http import HttpResponse

from document_upload.models import *

def get_data_permanentes(date):
    # Obtener los objetos de infoPlanilla filtrados por año y mes
    info_planilla = infoPlanilla.objects.filter(periodo=date)
    return info_planilla