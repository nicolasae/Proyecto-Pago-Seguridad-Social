from django.shortcuts import render, redirect
from django.utils.encoding import escape_uri_path

from document_upload.models import *
from .report_planilla import *
from .report_temporales import *
from .report_permanentes import *

def download_view(request):
    if request.method == 'POST':
        selected_year = request.POST.get('selectYear')
        selected_month = request.POST.get('selectMonth')

        if 'btn_resumen_planilla' in request.POST:
            # Acción para generar el resumen de la planilla
            return create_report_planilla(selected_year,selected_month)
        
        if 'btn_resumen_patronales_temporales' in request.POST:
            # Aquí puedes realizar la acción para generar el resumen de las patronales           
            return create_report_temporales(selected_year, selected_month)
           
    return redirect('reportes')

def create_report_planilla(year,month):
    date = year + '/' + month
    info_planilla = get_info_planilla(date)
    values_planilla = get_values_planilla(date)
    return generate_excel_report(info_planilla,values_planilla, year, month)
   

def create_report_temporales(year, month):
    date = year + '/' + month
    data_temporales = get_data_temporales(date)
    return generate_excel_report_temporales(data_temporales, year, month)



