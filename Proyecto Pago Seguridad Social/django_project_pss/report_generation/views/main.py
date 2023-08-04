from django.shortcuts import render, redirect
from django.contrib import messages

from document_upload.models import *
from .report_planilla import *
from .report_patronales import *
from .report_temporales import *
from .report_permanentes import *

def download_view(request):
    if request.method == 'POST':
        selected_year = request.POST.get('selectYear')
        selected_month = request.POST.get('selectMonth')

        if 'btn_resumen_planilla' in request.POST:
            return create_report_planilla(request, selected_year, selected_month)
           
        if 'btn_resumen_patronales' in request.POST:
            return create_report_patronales(request, selected_year, selected_month)
        
        if 'btn_resumen_patronales_temporales' in request.POST:
            return create_report_temporales(request, selected_year, selected_month)
        
        if 'btn_resumen_patronales_permanentes' in request.POST:
            return create_report_permanentes(request, selected_year, selected_month)           
    
    return render(request, 'reports.html')


def create_report_planilla(request,year,month):
    date = year + '/' + month
    info_planilla = get_info_planilla(date)

    if info_planilla.exists():
        values_planilla = get_values_planilla(date)       
        return generate_excel_report(info_planilla,values_planilla, year, month)
    else:
        context = {
            'show_alert': True,
            'alert_type':"danger",
            'message':f'No hay información disponible de la planilla del periodo: {date}.',
        }        
        return render(request, 'reports.html', context)
    
def create_report_patronales(request, year, month):
    date = year + '/' + month
    data = get_data_patronales(date)
    
    if len(data) > 0:
        return generate_excel_report_patronales(data,year,month)
    else:
        context = {
            'show_alert': True,
            'alert_type':"danger",
            'message':f'No hay información disponible de patronales para el periodo: {date}.',
        }        
        return render(request, 'reports.html', context)

def create_report_temporales(request,year,month):
    date = year + '/' + month
    data_temporales = get_data_temporales(date)

    if len(data_temporales) > 0:
        return generate_excel_report_temporales(data_temporales, year, month)
    else:
        context = {
            'show_alert': True,
            'alert_type':"danger",
            'message':f'No hay información disponible de patronales temporales para el periodo: {date}.',
        }        
        return render(request, 'reports.html', context)

def create_report_permanentes(request,year, month):
    date = year + '/' + month
    data_permanentes = get_data_permanentes(date)

    if (len(data_permanentes) > 0):
        return generate_excel_report_permanentes(data_permanentes, year, month)
    else:
        context = {
            'show_alert': True,
            'alert_type':"danger",
            'message':f'No hay información disponible de patronales permanentes para el periodo: {date}.',
        }        
        return render(request, 'reports.html', context)


